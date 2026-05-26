from flask import Flask, render_template, request, jsonify, session, send_file, redirect, url_for
import random
import re
import bcrypt
import io
import os
import json
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
import hashlib

# ============ NEW IMPORTS FOR DOCUMENT ANALYSIS ============
from langchain_community.document_loaders import PyMuPDFLoader, WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import tempfile
import time

app = Flask(__name__)
app.secret_key = 'linkenai_secret_key_2026'
app.permanent_session_lifetime = timedelta(days=7)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

# Create upload folders
UPLOAD_FOLDER = 'uploads'
RESUME_FOLDER = 'resumes'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESUME_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESUME_FOLDER'] = RESUME_FOLDER

# ============ USER DATABASE ============
USERS_FILE = 'users.json'

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

# ============ DOCUMENT ANALYSIS WITH VECTOR STORE ============
# Store vectorstores per session
vector_stores = {}
document_summaries = {}
document_stats = {}
suggested_questions = {}

def process_document(file_content, filename):
    """Process PDF document and create vector store"""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            tmp.write(file_content)
            tmp_path = tmp.name
        
        # Load document
        loader = PyMuPDFLoader(tmp_path)
        documents = loader.load()
        os.unlink(tmp_path)
        
        # Split into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_documents(documents)
        
        # Create embeddings and vector store
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vectorstore = FAISS.from_documents(chunks, embeddings)
        
        # Calculate stats
        total_chars = sum([len(doc.page_content) for doc in documents])
        total_words = total_chars // 5
        
        stats = {
            "pages": len(documents),
            "characters": total_chars,
            "words": total_words,
            "reading_time": max(1, total_words // 200),
            "name": filename
        }
        
        # Generate summary from first few chunks
        summary_text = " ".join([doc.page_content[:500] for doc in documents[:3]])
        summary = summary_text[:500] + "..." if len(summary_text) > 500 else summary_text
        
        # Generate suggested questions
        first_words = documents[0].page_content.split()[:50] if documents else []
        suggestions = [
            f"What is the main topic of this document?",
            "Can you summarize the key points?",
            f"What does the document say about the main subject?",
            "What are the most important conclusions?",
            "Can you explain the main ideas in simple terms?"
        ]
        
        return {
            'success': True,
            'vectorstore': vectorstore,
            'stats': stats,
            'summary': summary,
            'suggestions': suggestions[:3],
            'documents': documents
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}

def process_url(url):
    """Process URL and create vector store"""
    try:
        loader = WebBaseLoader(url)
        documents = loader.load()
        
        # Split into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_documents(documents)
        
        # Create embeddings and vector store
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vectorstore = FAISS.from_documents(chunks, embeddings)
        
        # Calculate stats
        total_chars = sum([len(doc.page_content) for doc in documents])
        total_words = total_chars // 5
        
        stats = {
            "pages": len(documents),
            "characters": total_chars,
            "words": total_words,
            "reading_time": max(1, total_words // 200),
            "name": url[:50] + "..."
        }
        
        # Generate summary
        summary_text = " ".join([doc.page_content[:500] for doc in documents[:3]])
        summary = summary_text[:500] + "..." if len(summary_text) > 500 else summary_text
        
        suggestions = [
            f"What is the main topic of this webpage?",
            "Can you summarize the key points?",
            "What are the most important conclusions?"
        ]
        
        return {
            'success': True,
            'vectorstore': vectorstore,
            'stats': stats,
            'summary': summary,
            'suggestions': suggestions[:3],
            'documents': documents
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}

def get_answer_from_document(question, vectorstore):
    """Search vector store for answer"""
    try:
        docs = vectorstore.similarity_search(question, k=3)
        if docs:
            # Combine top results
            answer = docs[0].page_content[:800]
            return {
                'success': True,
                'answer': answer,
                'sources': [doc.page_content[:300] + "..." for doc in docs[1:]] if len(docs) > 1 else []
            }
        return {'success': False, 'error': 'No relevant information found'}
    except Exception as e:
        return {'success': False, 'error': str(e)}

# ============ TEXT EXTRACTION FROM PDF (for ATS) ============
def extract_text_from_pdf(file_content):
    """Extract text from PDF file content"""
    try:
        import PyPDF2
        from io import BytesIO
        pdf_file = BytesIO(file_content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    except Exception as e:
        print(f"PDF extraction error: {str(e)}")
        return ""

# ============ ATS SCORE CALCULATION ============
def calculate_ats_score(resume_text):
    """Calculate accurate ATS score based on resume content"""
    if not resume_text or len(resume_text.strip()) < 100:
        return {
            'score': 0,
            'rating': 'Poor',
            'rating_message': 'Resume too short. Please upload a valid resume.',
            'word_count': len(resume_text.split()) if resume_text else 0,
            'skills_count': 0,
            'action_verbs': 0,
            'sections_found': 0,
            'feedback': ['❌ Resume content too short for analysis'],
            'suggestions': ['Add more details to your experience, education, and skills sections']
        }
    
    text = resume_text.lower()
    word_count = len(resume_text.split())
    
    # Keyword libraries
    tech_keywords = ['python', 'java', 'javascript', 'react', 'angular', 'vue', 'node', 'html', 'css', 
                     'sql', 'mongodb', 'git', 'docker', 'aws', 'azure', 'api', 'django', 'flask', 
                     'spring', 'c++', 'php', 'ruby', 'go', 'tensorflow', 'pytorch', 'pandas', 'numpy',
                     'machine learning', 'data analysis', 'linux', 'android', 'ios']
    
    soft_keywords = ['leadership', 'communication', 'teamwork', 'problem solving', 'critical thinking', 
                     'time management', 'adaptability', 'creativity', 'collaboration', 'analytical',
                     'project management', 'organized', 'detail oriented']
    
    action_verbs = ['achieved', 'improved', 'increased', 'developed', 'created', 'built', 'designed',
                    'implemented', 'launched', 'led', 'managed', 'coordinated', 'analyzed', 'optimized',
                    'solved', 'resolved', 'trained', 'mentored']
    
    sections = ['summary', 'experience', 'education', 'skills', 'projects', 'certifications']
    
    # Calculate metrics
    found_tech = sum(1 for kw in tech_keywords if kw in text)
    found_soft = sum(1 for kw in soft_keywords if kw in text)
    found_verbs = sum(1 for v in action_verbs if v in text)
    found_sections = sum(1 for s in sections if s in text)
    
    total_keywords = found_tech + found_soft
    
    # Score calculations
    keyword_score = min(100, (total_keywords / 15) * 100)
    verb_score = min(100, (found_verbs / 8) * 100)
    section_score = (found_sections / len(sections)) * 100
    
    # Length score
    if 400 <= word_count <= 800:
        length_score = 100
    elif word_count < 300:
        length_score = (word_count / 300) * 70
    elif word_count > 1000:
        length_score = max(70, 100 - ((word_count - 800) / 800) * 30)
    else:
        length_score = 85
    
    # Quantifiable achievements
    quant_score = 50
    if '%' in text:
        quant_score += 25
    if re.search(r'\b\d{2,}\b', text):
        quant_score += 25
    quant_score = min(100, quant_score)
    
    # Contact info
    contact_score = 0
    if re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', resume_text):
        contact_score += 50
    if re.search(r'\b\d{10}\b|\+\d{1,3}\s?\d{10}\b', resume_text):
        contact_score += 50
    
    # Final score
    final_score = int((keyword_score * 0.35) + (verb_score * 0.20) + (section_score * 0.15) + 
                      (length_score * 0.10) + (quant_score * 0.10) + (contact_score * 0.10))
    final_score = max(0, min(100, final_score))
    
    # Rating
    if final_score >= 80:
        rating = "Excellent"
        rating_message = "🎯 Excellent! Your resume is highly optimized for ATS systems."
    elif final_score >= 65:
        rating = "Good"
        rating_message = "✅ Good! Minor improvements needed."
    elif final_score >= 50:
        rating = "Fair"
        rating_message = "⚠️ Needs moderate improvements."
    else:
        rating = "Needs Improvement"
        rating_message = "🔧 Needs significant improvements."
    
    # Feedback
    feedback = []
    suggestions = []
    
    if total_keywords >= 12:
        feedback.append(f"✅ Good keyword presence ({total_keywords} keywords)")
    else:
        suggestions.append(f"🔑 Add more relevant keywords like: Python, Java, React, SQL")
    
    if found_verbs >= 6:
        feedback.append(f"✅ Good action verb usage ({found_verbs} verbs)")
    else:
        suggestions.append(f"📝 Use action verbs: Developed, Led, Implemented, Achieved")
    
    if found_sections >= 4:
        feedback.append(f"✅ Good section structure ({found_sections}/6 sections)")
    else:
        suggestions.append(f"📋 Add sections: Experience, Education, Skills, Projects")
    
    if 400 <= word_count <= 800:
        feedback.append(f"✅ Optimal length ({word_count} words)")
    elif word_count < 400:
        suggestions.append(f"📄 Increase length to 400-800 words (currently {word_count})")
    
    # Keywords found
    keywords_found = []
    for kw in tech_keywords[:15]:
        if kw in text:
            keywords_found.append(kw)
    for kw in soft_keywords[:8]:
        if kw in text and kw not in keywords_found:
            keywords_found.append(kw)
    
    return {
        'score': final_score,
        'rating': rating,
        'rating_message': rating_message,
        'word_count': word_count,
        'skills_count': total_keywords,
        'action_verbs': found_verbs,
        'sections_found': found_sections,
        'feedback': feedback[:4],
        'suggestions': suggestions[:4],
        'keywords_found': keywords_found[:20]
    }

# ============ FLASK ROUTES ============

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin-dashboard')
def admin_dashboard():
    if session.get('role') != 'admin':
        return redirect(url_for('home'))
    return render_template('admin_dashboard.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username', '')
    phone = data.get('phone', '')
    email = data.get('email', '')
    password = data.get('password', '')
    
    if not username or not phone or not email or not password:
        return jsonify({'success': False, 'message': 'All fields required'}), 400
    
    users = load_users()
    
    if username in users:
        return jsonify({'success': False, 'message': 'Username already exists'}), 400
    
    users[username] = {
        'username': username,
        'phone': phone,
        'email': email,
        'password': password,
        'role': 'user',
        'joinDate': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    save_users(users)
    return jsonify({'success': True, 'message': 'Registration successful'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')
    
    # Admin login
    if username == 'admin' and password == 'admin123':
        session.permanent = True
        session['logged_in'] = True
        session['username'] = username
        session['role'] = 'admin'
        session['session_id'] = str(datetime.now().timestamp())
        
        return jsonify({
            'success': True,
            'username': username,
            'role': 'admin',
            'redirect': '/admin-dashboard'
        })
    
    # User login
    users = load_users()
    stored_user = users.get(username)
    
    if stored_user and stored_user.get('password') == password:
        session.permanent = True
        session['logged_in'] = True
        session['username'] = username
        session['role'] = 'user'
        session['session_id'] = str(datetime.now().timestamp())
        
        return jsonify({
            'success': True,
            'username': username,
            'role': 'user'
        })
    
    return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True})

@app.route('/check_session', methods=['GET'])
def check_session():
    return jsonify({
        'logged_in': session.get('logged_in', False),
        'username': session.get('username'),
        'role': session.get('role', 'user')
    })

# ============ CHAT ROUTE ==========
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message', '')
    
    q = message.lower()
    
    if any(word in q for word in ["hi", "hello", "hey"]):
        response = "👋 Hello! I'm your AI Career Assistant. I can help with:\n\n• Career guidance\n• Resume tips\n• Interview preparation\n• Skills recommendations\n\nWhat would you like help with today?"
    elif "resume" in q:
        response = "📄 **Resume Tips:**\n\n✅ Keep it ATS-friendly\n✅ Use action verbs\n✅ Quantify achievements\n✅ Include relevant keywords\n✅ Keep length 1-2 pages"
    elif "interview" in q:
        response = "🎤 **Interview Tips:**\n\n⭐ Research the company\n⭐ Practice common questions\n⭐ Prepare questions to ask\n⭐ Dress professionally\n⭐ Follow up with thank you email"
    elif "bca" in q:
        response = "💻 **BCA Career Paths:**\n\n• Software Developer\n• Web Developer\n• Data Analyst\n• Cyber Security Analyst\n• Cloud Engineer"
    elif "mca" in q:
        response = "🖥️ **MCA Career Paths:**\n\n• Software Engineer\n• Full Stack Developer\n• AI/ML Engineer\n• Cloud Architect\n• Technical Lead"
    else:
        response = f"🤖 I'm here to help with career guidance. Could you please specify what you'd like to know about? For example: resume tips, interview preparation, BCA/MCA career paths, or skills to learn."
    
    return jsonify({'response': response})

# ============ POST GENERATOR ROUTE ==========
@app.route('/generate_post', methods=['POST'])
def generate_post():
    data = request.get_json()
    topic = data.get('topic', '')
    tone = data.get('tone', 'professional')
    
    if not topic:
        return jsonify({'error': 'Please enter a topic'}), 400
    
    if tone == "professional":
        post = f"""🚀 **The Strategic Importance of {topic.title()}**

In today's rapidly evolving landscape, {topic.lower()} has emerged as a critical driver of innovation and growth.

What are your thoughts on this trend? Share below! 👇

---
#{topic.lower().replace(' ', '')} #Innovation #Leadership"""
    
    elif tone == "casual":
        post = f"""Hey everyone! 👋

Been thinking a lot about {topic.lower()} lately. It's amazing how this space is evolving!

What's YOUR experience? Drop a comment! 🙌

---
#{topic.lower().replace(' ', '')} #RealTalk"""
    
    else:
        post = f"""✨ **The {topic.title()} Journey** ✨

Every expert was once a beginner. Your journey with {topic.lower()} starts with a single step.

Take action today. Your future self will thank you. 💪

---
#{topic.lower().replace(' ', '')} #Motivation #GrowthMindset"""
    
    return jsonify({'post': post})

# ============ COMMENT ANALYZER ROUTE ==========
@app.route('/reply', methods=['POST'])
def reply():
    data = request.get_json()
    comment = data.get('comment', '')
    
    comment_lower = comment.lower()
    positive_words = ['good', 'great', 'excellent', 'amazing', 'nice', 'awesome', 'love', 'like']
    negative_words = ['bad', 'terrible', 'awful', 'hate', 'dislike', 'poor', 'useless']
    
    pos_count = sum(1 for w in positive_words if w in comment_lower)
    neg_count = sum(1 for w in negative_words if w in comment_lower)
    
    if pos_count > neg_count:
        sentiment = 'positive'
        sentiment_icon = '😊'
        reply = "Thank you for your positive feedback! I appreciate your support! 🙏"
    elif neg_count > pos_count:
        sentiment = 'negative'
        sentiment_icon = '😞'
        reply = "Thank you for your feedback. How can I help you better with your career goals?"
    else:
        sentiment = 'neutral'
        sentiment_icon = '😐'
        reply = "Thanks for sharing your thoughts! Let me know if you have any career questions."
    
    return jsonify({
        'success': True,
        'sentiment': sentiment,
        'sentiment_icon': sentiment_icon,
        'reply': reply
    })

# ============ UPDATED: DOCUMENT UPLOAD ROUTE (with Vector Store) ==========
@app.route('/upload/document', methods=['POST'])
def upload_document():
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        if not file.filename.lower().endswith('.pdf'):
            return jsonify({'success': False, 'error': 'Only PDF files are supported'}), 400
        
        session_id = session.get('session_id')
        if not session_id:
            session['session_id'] = str(datetime.now().timestamp())
            session_id = session.get('session_id')
        
        file_content = file.read()
        
        # Process document with LangChain
        result = process_document(file_content, file.filename)
        
        if result['success']:
            vector_stores[session_id] = result['vectorstore']
            document_stats[session_id] = result['stats']
            document_summaries[session_id] = result['summary']
            suggested_questions[session_id] = result['suggestions']
            
            # Also extract text for ATS if needed
            resume_text = extract_text_from_pdf(file_content)
            
            return jsonify({
                'success': True,
                'message': f'✅ "{file.filename}" uploaded and processed!',
                'metadata': result['stats'],
                'summary': result['summary'],
                'suggestions': result['suggestions'],
                'content': resume_text[:500] if resume_text else ""
            })
        else:
            return jsonify({'success': False, 'error': result['error']}), 500
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============ UPDATED: URL UPLOAD ROUTE ==========
@app.route('/upload/url', methods=['POST'])
def upload_url():
    try:
        data = request.get_json()
        url = data.get('url', '')
        
        if not url:
            return jsonify({'success': False, 'error': 'No URL provided'}), 400
        
        session_id = session.get('session_id')
        if not session_id:
            session['session_id'] = str(datetime.now().timestamp())
            session_id = session.get('session_id')
        
        result = process_url(url)
        
        if result['success']:
            vector_stores[session_id] = result['vectorstore']
            document_stats[session_id] = result['stats']
            document_summaries[session_id] = result['summary']
            suggested_questions[session_id] = result['suggestions']
            
            return jsonify({
                'success': True,
                'message': f'✅ URL content loaded successfully!',
                'metadata': result['stats'],
                'summary': result['summary'],
                'suggestions': result['suggestions']
            })
        else:
            return jsonify({'success': False, 'error': result['error']}), 500
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ============ DOCUMENT STATUS ROUTE ==========
@app.route('/document/status', methods=['GET'])
def document_status():
    session_id = session.get('session_id')
    
    if session_id and session_id in vector_stores:
        stats = document_stats.get(session_id, {})
        return jsonify({
            'success': True,
            'has_document': True,
            'metadata': {
                'name': stats.get('name', 'Document'),
                'pages': stats.get('pages', 1),
                'words': stats.get('words', 0),
                'reading_time': stats.get('reading_time', 1)
            },
            'summary': document_summaries.get(session_id, ''),
            'suggestions': suggested_questions.get(session_id, [])
        })
    
    return jsonify({'success': True, 'has_document': False})

# ============ DOCUMENT DELETE ROUTE ==========
@app.route('/document/delete', methods=['POST'])
def delete_document():
    session_id = session.get('session_id')
    
    if session_id:
        if session_id in vector_stores:
            del vector_stores[session_id]
        if session_id in document_stats:
            del document_stats[session_id]
        if session_id in document_summaries:
            del document_summaries[session_id]
        if session_id in suggested_questions:
            del suggested_questions[session_id]
    
    return jsonify({'success': True, 'message': 'Document deleted successfully'})

# ============ UPDATED: DOCUMENT ASK ROUTE (with Vector Search) ==========
@app.route('/document/ask', methods=['POST'])
def document_ask():
    try:
        data = request.get_json()
        question = data.get('question', '')
        session_id = session.get('session_id')
        
        if not session_id or session_id not in vector_stores:
            return jsonify({
                'response': "📄 **No Document Loaded**\n\nPlease upload a PDF document or URL first before asking questions."
            })
        
        vectorstore = vector_stores[session_id]
        result = get_answer_from_document(question, vectorstore)
        
        if result['success']:
            response_text = f"📖 **Answer:**\n\n{result['answer']}"
            if result['sources']:
                response_text += f"\n\n📚 **Additional Sources:**\n"
                for i, src in enumerate(result['sources'][:2], 1):
                    response_text += f"\n**Source {i}:** {src}"
            return jsonify({'response': response_text})
        else:
            return jsonify({'response': f"❌ {result['error']}\n\n💡 Try rephrasing your question or asking about a different topic in the document."})
        
    except Exception as e:
        return jsonify({'response': f"Error: {str(e)}"}), 500

# ============ GET SUGGESTED QUESTIONS ROUTE ==========
@app.route('/get_suggested_questions', methods=['GET'])
def get_suggested_questions():
    session_id = session.get('session_id')
    
    if session_id and session_id in suggested_questions:
        return jsonify({'success': True, 'questions': suggested_questions[session_id]})
    
    return jsonify({'success': False, 'questions': []})

# ============ GENERATE OBJECTIVE ROUTE ==========
@app.route('/generate_dynamic_objective', methods=['POST'])
def generate_dynamic_objective():
    try:
        data = request.get_json()
        role = data.get('role', '')
        obj_type = data.get('obj_type', 'technical')
        
        if not role:
            return jsonify({'error': 'Please enter a job role'}), 400
        
        if obj_type == 'technical':
            objective = f"Results-driven {role} with strong technical skills. Passionate about building scalable solutions and solving complex challenges. Seeking an opportunity to leverage expertise and contribute to innovative projects."
        elif obj_type == 'management':
            objective = f"Strategic {role} with proven leadership abilities. Expertise in team management, project delivery, and process optimization. Seeking to drive organizational growth and deliver exceptional results."
        else:
            objective = f"Dynamic {role} combining technical expertise with leadership capabilities. Passionate about bridging technology and business objectives for optimal results."
        
        return jsonify({'success': True, 'objective': objective})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============ GET ATS SCORE ROUTE ==========
@app.route('/get_ats_score', methods=['GET', 'POST'])
def get_ats_score():
    try:
        data = request.get_json() if request.method == 'POST' else {}
        resume_text = data.get('resume_text', '')
        
        # Also check if we have document content
        session_id = session.get('session_id')
        if session_id and session_id in vector_stores and not resume_text:
            # Try to get text from vector store documents
            pass
        
        if not resume_text or len(resume_text.strip()) < 100:
            return jsonify({
                'success': False,
                'error': 'No resume content. Please upload a resume first.',
                'score': 0,
                'rating': 'No Resume',
                'rating_message': 'Please upload a resume to get an ATS score'
            })
        
        result = calculate_ats_score(resume_text)
        
        return jsonify({
            'success': True,
            'score': result['score'],
            'rating': result['rating'],
            'rating_message': result['rating_message'],
            'feedback': result['feedback'],
            'suggestions': result['suggestions'],
            'stats': {
                'word_count': result['word_count'],
                'skills_count': result['skills_count'],
                'action_verbs': result['action_verbs'],
                'sections_found': result['sections_found']
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============ UPDATE RESUME PDF ROUTE ==========
@app.route('/update_resume_pdf', methods=['POST'])
def update_resume_pdf():
    try:
        data = request.get_json()
        
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        from reportlab.lib.utils import simpleSplit
        
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        
        c.setFont("Helvetica-Bold", 20)
        c.setFillColorRGB(0.4, 0.42, 0.68)
        c.drawString(50, height - 50, "PROFESSIONAL RESUME")
        
        c.setFont("Helvetica-Bold", 16)
        c.setFillColorRGB(0, 0, 0)
        name = data.get('name', 'Your Name')
        c.drawString(50, height - 90, name)
        
        c.setFont("Helvetica", 10)
        y = height - 115
        c.drawString(50, y, f"📧 {data.get('email', 'email@example.com')}")
        c.drawString(250, y, f"📞 {data.get('phone', '+91 XXXXX XXXXX')}")
        c.drawString(450, y, f"📍 {data.get('location', 'India')}")
        
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, height - 150, "PROFESSIONAL OBJECTIVE")
        c.setFont("Helvetica", 10)
        objective = data.get('objective', '')
        lines = simpleSplit(objective, 'Helvetica', 10, width - 100)
        y = height - 170
        for line in lines[:4]:
            c.drawString(50, y, line)
            y -= 15
        
        y -= 10
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "TECHNICAL SKILLS")
        c.setFont("Helvetica", 10)
        y -= 20
        skills = data.get('skills', [])
        skills_text = ', '.join(skills[:10])
        lines = simpleSplit(skills_text, 'Helvetica', 10, width - 100)
        for line in lines:
            c.drawString(50, y, f"• {line}")
            y -= 15
        
        c.save()
        buffer.seek(0)
        
        return send_file(buffer, as_attachment=True, download_name='My_Resume.pdf', mimetype='application/pdf')
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============ GET INTERVIEW QUESTIONS ROUTE ==========
@app.route('/get_interview_questions', methods=['POST'])
def get_interview_questions():
    data = request.get_json()
    category = data.get('category', 'developer')
    
    questions = {
        "developer": [
            {"q": "What is your experience with full-stack development?", "a": "I have worked on multiple full-stack projects using React and Node.js."},
            {"q": "How do you handle tight deadlines?", "a": "I prioritize tasks based on impact and urgency."}
        ],
        "behavioral": [
            {"q": "Tell me about a challenge you overcame.", "a": "Using the STAR method: Situation, Task, Action, Result."}
        ],
        "hr": [
            {"q": "What are your salary expectations?", "a": "Based on market research and my experience."}
        ]
    }
    
    return jsonify({
        'success': True,
        'data': questions.get(category, questions['developer'])
    })

# ============ GET COLOR THEMES ROUTE ==========
@app.route('/get_color_themes', methods=['GET'])
def get_color_themes():
    themes = {
        "professional_blue": {"primary": "#1a5276", "secondary": "#2980b9", "accent": "#3498db", "name": "Professional Blue"},
        "corporate_navy": {"primary": "#0a192f", "secondary": "#172a45", "accent": "#64ffda", "name": "Corporate Navy"},
        "elegant_green": {"primary": "#0b3d3f", "secondary": "#1a6b6e", "accent": "#2ecc71", "name": "Elegant Green"}
    }
    return jsonify({'success': True, 'themes': themes})

# ============ TRACK PAGE ROUTE ==========
@app.route('/track/page', methods=['POST'])
def track_page():
    return jsonify({'success': True})

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🤖 LINKENAI PRO - COMPLETE RESUME EDITOR")
    print("=" * 60)
    print("\n🔐 User Login: Register as new user")
    print("👑 Admin Login: admin / admin123")
    print("🌐 Open: http://localhost:5000")
    print("=" * 60 + "\n")
    app.run(debug=True)