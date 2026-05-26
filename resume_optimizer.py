# resume_optimizer.py
import streamlit as st
import re
from collections import Counter
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Resume Optimizer AI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .main-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 30px;
        margin: 20px auto;
        max-width: 1200px;
    }
    
    .gradient-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
    }
    
    .result-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .keyword-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 5px 12px;
        border-radius: 20px;
        display: inline-block;
        margin: 3px;
        font-size: 12px;
    }
    
    .match-score {
        font-size: 48px;
        font-weight: bold;
        text-align: center;
        margin: 20px;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 10px 30px;
        font-size: 16px;
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("""
<h1 style="text-align: center; font-size: 60px; margin-bottom: 0;">
    <span class="gradient-header">📄 Resume Optimizer AI</span>
</h1>
<p style="text-align: center; color: #e0e0e0; font-size: 18px;">
    Paste your resume + job description → Get optimized resume instantly
</p>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Main container
with st.container():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Layout: Two columns for input
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📄 Your Current Resume")
        st.markdown("*Paste your existing resume text here*")
        
        resume_text = st.text_area(
            "",
            height=400,
            placeholder="""
Example:
Senior Data Analyst with 5+ years of experience in Python, SQL, and Tableau.
Led data analytics projects resulting in 20% efficiency improvement.
Strong background in statistical analysis and data visualization.
Bachelor's Degree in Computer Science.
            """.strip(),
            label_visibility="collapsed"
        )
        
        # Resume format options
        with st.expander("📝 Resume Formatting Options"):
            st.info("""
            **Tips for better results:**
            - Include your skills section clearly
            - List work experience with action verbs
            - Add education and certifications
            - Mention tools and technologies
            """)
    
    with col2:
        st.markdown("### 🎯 Job Description")
        st.markdown("*Paste the target job description here*")
        
        jd_text = st.text_area(
            "",
            height=400,
            placeholder="""
Example:
We are looking for a Data Analyst who can:
- Analyze complex datasets using Python and SQL
- Create dashboards in Tableau/Power BI
- Provide data-driven insights for business decisions
- Strong communication and presentation skills
Required: Bachelor's degree in related field
            """.strip(),
            label_visibility="collapsed"
        )
        
        # Additional context
        with st.expander("⚙️ Optimization Settings"):
            col_a, col_b = st.columns(2)
            with col_a:
                optimization_level = st.select_slider(
                    "Optimization Intensity",
                    options=["Conservative", "Balanced", "Aggressive"],
                    value="Balanced"
                )
            with col_b:
                include_cover_letter = st.checkbox("Generate cover letter too", value=False)

    # Analyze Button
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        analyze_button = st.button("🚀 Optimize My Resume", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Process and display results
if analyze_button:
    if not resume_text.strip():
        st.error("❌ Please paste your resume text!")
    elif not jd_text.strip():
        st.error("❌ Please paste the job description!")
    else:
        with st.spinner("🔍 Analyzing and optimizing your resume..."):
            
            # Extract keywords from JD
            def extract_keywords(text):
                # Remove common words
                stop_words = {'and', 'or', 'the', 'a', 'an', 'of', 'to', 'for', 'in', 'on', 'at', 'with', 'by', 
                             'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having',
                             'do', 'does', 'did', 'doing', 'but', 'not', 'so', 'get', 'we', 'they', 'this', 'that',
                             'these', 'those', 'from', 'as', 'into', 'like', 'just', 'over', 'such', 'can', 'will',
                             'our', 'your', 'their', 'about', 'than', 'then', 'now', 'only', 'very', 'when', 'where',
                             'there', 'their', 'would', 'could', 'should'}
                
                words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
                words = [w for w in words if w not in stop_words]
                
                # Count frequencies
                word_counts = Counter(words)
                
                # Get top keywords
                keywords = [word for word, count in word_counts.most_common(20)]
                return keywords, word_counts
            
            jd_keywords, jd_counts = extract_keywords(jd_text)
            resume_keywords, resume_counts = extract_keywords(resume_text)
            
            # Calculate match score
            matched_keywords = set(jd_keywords) & set(resume_keywords)
            match_score = int((len(matched_keywords) / max(len(jd_keywords), 1)) * 100)
            
            # Find missing keywords
            missing_keywords = [kw for kw in jd_keywords if kw not in resume_keywords]
            
            # Generate optimized resume
            def optimize_resume(resume, jd, keywords_to_add, level="Balanced"):
                optimized = resume
                
                # Add missing keywords strategically
                if level == "Conservative":
                    keywords_to_add = keywords_to_add[:5]
                elif level == "Balanced":
                    keywords_to_add = keywords_to_add[:10]
                else:  # Aggressive
                    keywords_to_add = keywords_to_add[:15]
                
                # Add skills section if missing
                if "skills" not in optimized.lower() and keywords_to_add:
                    optimized += f"\n\n**Skills:** {', '.join(keywords_to_add)}"
                else:
                    # Inject keywords into existing sections
                    for kw in keywords_to_add:
                        if kw not in optimized.lower():
                            # Add to skills section or create one
                            if "skills:" in optimized.lower():
                                optimized = optimized.replace("Skills:", f"Skills: {kw.title()}, ", 1)
                            else:
                                optimized += f"\n- {kw.title()}"
                
                return optimized
            
            optimized_resume = optimize_resume(resume_text, jd_text, missing_keywords, optimization_level)
            
            # Generate cover letter if requested
            cover_letter = ""
            if include_cover_letter:
                cover_letter = f"""
Dear Hiring Manager,

I am writing to express my interest in the position. With my background in {', '.join(jd_keywords[:5])}, I am confident in my ability to contribute to your team.

My experience aligns perfectly with your requirements, particularly in {matched_keywords[0] if matched_keywords else 'data analysis'}. I am excited about the opportunity to bring my skills in {', '.join(list(matched_keywords)[:3])} to your organization.

Thank you for considering my application.

Sincerely,
[Your Name]
                """
            
            # Display Results
            st.markdown("---")
            st.markdown("## 📊 Analysis Results")
            
            # Match Score Card
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                score_color = "🟢" if match_score >= 70 else "🟡" if match_score >= 40 else "🔴"
                st.markdown(f"""
                <div class="result-card" style="text-align: center;">
                    <h3>Resume Match Score</h3>
                    <div class="match-score" style="color: {'#27ae60' if match_score >= 70 else '#f39c12' if match_score >= 40 else '#e74c3c'}">
                        {score_color} {match_score}%
                    </div>
                    <p>{len(matched_keywords)} out of {len(jd_keywords)} keywords matched</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Keywords Section
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### ✅ Keywords Found in Your Resume")
                if matched_keywords:
                    for kw in matched_keywords[:15]:
                        st.markdown(f'<span class="keyword-badge">✓ {kw}</span>', unsafe_allow_html=True)
                else:
                    st.warning("No matching keywords found. Consider adding skills from job description.")
            
            with col2:
                st.markdown("### ⚠️ Missing Keywords to Add")
                if missing_keywords:
                    for kw in missing_keywords[:15]:
                        st.markdown(f'<span class="keyword-badge" style="background: #e74c3c;">+ {kw}</span>', unsafe_allow_html=True)
                    st.info(f"📝 Add these {len(missing_keywords[:15])}+ keywords to improve your match score")
                else:
                    st.success("Great job! Your resume matches well with this job!")
            
            # Optimized Resume
            st.markdown("---")
            st.markdown("## ✨ Your Optimized Resume")
            
            with st.expander("📄 Click to view optimized resume", expanded=True):
                st.markdown("### Optimized Resume")
                st.text_area(
                    "Copy this optimized resume",
                    optimized_resume,
                    height=400,
                    key="optimized_resume"
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📋 Copy to Clipboard", use_container_width=True):
                        st.success("✅ Resume copied! (Press Ctrl+C to copy manually)")
                with col2:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    st.download_button(
                        label="💾 Download as TXT",
                        data=optimized_resume,
                        file_name=f"optimized_resume_{timestamp}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
            
            # Cover Letter (if requested)
            if include_cover_letter:
                st.markdown("---")
                st.markdown("## 📝 Generated Cover Letter")
                with st.expander("📄 Click to view cover letter", expanded=True):
                    st.text_area(
                        "Copy this cover letter",
                        cover_letter,
                        height=300,
                        key="cover_letter"
                    )
                    
                    st.download_button(
                        label="💾 Download Cover Letter",
                        data=cover_letter,
                        file_name=f"cover_letter_{timestamp}.txt",
                        mime="text/plain"
                    )
            
            # Tips to Improve
            st.markdown("---")
            st.markdown("## 💡 Tips to Improve Your Resume")
            
            tips = []
            if match_score < 50:
                tips.append("• Add specific skills mentioned in the job description")
                tips.append("• Use action verbs from the job posting")
                tips.append("• Quantify your achievements with numbers")
            elif match_score < 70:
                tips.append("• Add 3-5 more keywords from the missing list")
                tips.append("• Tailor your professional summary to match the role")
            else:
                tips.append("• Your resume is well-optimized! Consider adding a portfolio link")
                tips.append("• Add specific projects that demonstrate these skills")
            
            for tip in tips:
                st.markdown(tip)
            
            # Export All
            st.markdown("---")
            st.markdown("### 📦 Export Complete Package")
            
            full_report = f"""
RESUME OPTIMIZATION REPORT
==========================
Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Match Score: {match_score}%

Keywords Found: {len(matched_keywords)}
Missing Keywords: {len(missing_keywords)}

Matched Keywords: {', '.join(matched_keywords[:20])}

Missing Keywords to Add: {', '.join(missing_keywords[:20])}

OPTIMIZED RESUME:
{optimized_resume}

{cover_letter if include_cover_letter else ""}
            """
            
            st.download_button(
                label="📥 Download Complete Report",
                data=full_report,
                file_name=f"resume_optimization_report_{timestamp}.txt",
                mime="text/plain",
                use_container_width=True
            )

# Footer
st.markdown("""
<div style="text-align: center; padding: 20px; margin-top: 40px;">
    <p style="color: #e0e0e0; font-size: 12px;">
        🔍 Resume Optimizer AI | Extract keywords from JD | Get optimized resume instantly
    </p>
</div>
""", unsafe_allow_html=True)