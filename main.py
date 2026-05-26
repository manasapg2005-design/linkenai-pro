#!/usr/bin/env python
"""
LinkenAI - LinkedIn Marketing System (Terminal Version)
Run this file to use the AI agents directly in the command line.
"""

import os
import sys
import time
from datetime import datetime

# Try to import agents, with fallback if modules not found
try:
    from agents.research_agent import research_topic
    from agents.writer_agent import write_post
    from agents.optimizer_agent import optimize_post
    AGENTS_AVAILABLE = True
except ImportError:
    AGENTS_AVAILABLE = False
    print("⚠️ Agent modules not found. Using built-in fallback functions.\n")

# ============ FALLBACK FUNCTIONS (if agents not available) ============
def fallback_research(topic):
    """Fallback research function"""
    return {
        "topic": topic,
        "audience": "LinkedIn professionals and career seekers",
        "trending": f"{topic} is becoming increasingly important in 2026",
        "key_points": [
            f"📈 {topic} can boost your career growth by 40-60%",
            f"🎯 Top companies are investing heavily in {topic}",
            f"📚 Learning {topic} takes just 30 minutes daily",
            f"💼 {topic} skills are transferable across industries"
        ]
    }

def fallback_write(research):
    """Fallback write function"""
    topic = research["topic"]
    audience = research["audience"]
    trending = research["trending"]
    points = research["key_points"]
    
    return f"""📢 **{topic.upper()}** - What You Need to Know!

{trending}

Here's what you need to know about {topic} for {audience}:

✅ {points[0]}

✅ {points[1]}

✅ {points[2]}

💡 Take Action Today!

👇 What's your take? Comment below!

#CareerGrowth #{topic.replace(' ', '')} #LinkedInLearning"""

def fallback_optimize(post):
    """Fallback optimize function"""
    hooks = [
        "🔥 STOP SCROLLING! This changes everything!",
        "💡 3 things nobody tells you about this:",
        "🚀 If you ignore this, you'll fall behind:"
    ]
    import random
    hook = random.choice(hooks)
    
    hashtags = "#LinkedInGrowth #CareerAdvice #ProfessionalDevelopment #Networking #Success"
    
    return f"""{hook}

{post}

---

👇 Drop a 💡 if this helped you!

{hashtags}"""

# ============ UTILITY FUNCTIONS ============
def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the application header"""
    print("\n" + "=" * 70)
    print(" " * 20 + "✨ LINKENAI - AI LINKEDIN MARKETING SYSTEM ✨")
    print("=" * 70)
    print(" " * 22 + "6 AI Agents Working Together")
    print(" " * 20 + "Research → Write → Optimize → Comment → Resume → Chat")
    print("=" * 70)
    print()

def print_agents_info():
    """Print information about all 6 AI agents"""
    print("\n" + "━" * 70)
    print("🤖 OUR 6 INTELLIGENT AI AGENTS")
    print("━" * 70)
    print("""
🔍 AGENT 1: RESEARCH AGENT
   • Finds trending topics on LinkedIn
   • Analyzes your target audience
   • Extracts key insights and keywords

✍️ AGENT 2: WRITER AGENT
   • Creates professional LinkedIn posts
   • Writes engaging hooks and captions
   • Adapts tone for your audience

⚡ AGENT 3: OPTIMIZER AGENT
   • Adds attention-grabbing hooks
   • Includes relevant hashtags
   • Adds calls to action (CTAs)

💬 AGENT 4: COMMENT AI AGENT
   • Analyzes comment sentiment
   • Detects positive/negative/questions
   • Generates professional replies

📄 AGENT 5: RESUME OPTIMIZER
   • Extracts keywords from job descriptions
   • Adds targeted keywords to your resume
   • Calculates ATS compatibility score

🤖 AGENT 6: VOICE NAVIGATOR
   • Answers career questions naturally
   • Provides real-time assistance
   • Guides through all features
""")
    print("━" * 70)

def print_menu():
    """Print the main menu"""
    print("\n" + "─" * 70)
    print("📌 MAIN MENU")
    print("─" * 70)
    print("""
1. 📝 Generate LinkedIn Post
2. 💬 Analyze Comment & Generate Reply
3. 📄 Optimize Resume with Job Description
4. 🤖 Chat with AI Navigator
5. ℹ️ About AI Agents
6. ❓ Help & Tips
7. 🚪 Exit
""")
    print("─" * 70)

def generate_post_terminal():
    """Generate a LinkedIn post from terminal input"""
    print("\n" + "─" * 70)
    print("📝 LINKEDIN POST GENERATOR")
    print("─" * 70)
    
    topic = input("\n💡 Enter your LinkedIn topic: ").strip()
    
    if not topic:
        print("\n❌ Please enter a topic!")
        return
    
    print("\n" + "▶" * 35)
    print("🔄 AI AGENTS WORKING...")
    print("▶" * 35)
    
    # Simulate agent processing with delays
    print("\n🔍 AGENT 1: Researching topic...")
    time.sleep(1)
    
    if AGENTS_AVAILABLE:
        research = research_topic(topic)
    else:
        research = fallback_research(topic)
    
    print(f"   ✓ Audience identified: {research['audience']}")
    print(f"   ✓ Key points extracted: {len(research['key_points'])} insights")
    
    print("\n✍️ AGENT 2: Writing post...")
    time.sleep(1)
    
    if AGENTS_AVAILABLE:
        post = write_post(research)
    else:
        post = fallback_write(research)
    
    print("   ✓ Draft generated")
    
    print("\n⚡ AGENT 3: Optimizing content...")
    time.sleep(1)
    
    if AGENTS_AVAILABLE:
        final_post = optimize_post(post)
    else:
        final_post = fallback_optimize(post)
    
    print("   ✓ Hook added")
    print("   ✓ Hashtags added")
    print("   ✓ CTA included")
    
    print("\n" + "=" * 70)
    print("✅ YOUR LINKEDIN POST (Ready to Publish)")
    print("=" * 70)
    print(final_post)
    print("\n" + "=" * 70)
    
    # Ask to copy
    copy_choice = input("\n📋 Copy to clipboard? (y/n): ").lower()
    if copy_choice == 'y':
        try:
            import pyperclip
            pyperclip.copy(final_post)
            print("✅ Copied to clipboard!")
        except ImportError:
            print("⚠️ pyperclip not installed. Select the text manually and press Ctrl+C to copy.")
    
    print("\n💡 PRO TIPS:")
    print("   • Post between 8-10 AM for best engagement")
    print("   • Add a relevant image to your post")
    print("   • Reply to comments within 1 hour")

def analyze_comment_terminal():
    """Analyze a comment and generate reply"""
    print("\n" + "─" * 70)
    print("💬 COMMENT ANALYZER & REPLY GENERATOR")
    print("─" * 70)
    
    comment = input("\n💬 Paste the comment here: ").strip()
    
    if not comment:
        print("\n❌ Please enter a comment!")
        return
    
    topic = input("\n📌 Topic of the post (optional): ").strip()
    
    print("\n" + "▶" * 35)
    print("🔄 ANALYZING COMMENT...")
    print("▶" * 35)
    
    time.sleep(1)
    
    # Detect sentiment
    comment_lower = comment.lower()
    
    print("\n🔍 AGENT 4: Analyzing sentiment...")
    
    # Simple sentiment detection
    positive_words = ["great", "good", "awesome", "amazing", "excellent", "helpful", "insightful", "love", "thank"]
    negative_words = ["bad", "wrong", "useless", "hate", "terrible", "awful", "disappointed", "worst"]
    
    positive_count = sum(1 for w in positive_words if w in comment_lower)
    negative_count = sum(1 for w in negative_words if w in comment_lower)
    is_question = "?" in comment_lower or any(w in comment_lower for w in ["how", "what", "why", "when", "which"])
    
    if negative_count > positive_count:
        sentiment = "😠 Negative"
        sentiment_color = "🔴"
    elif positive_count > negative_count:
        sentiment = "😊 Positive"
        sentiment_color = "🟢"
    elif is_question:
        sentiment = "🤔 Question"
        sentiment_color = "🟡"
    else:
        sentiment = "😐 Neutral"
        sentiment_color = "⚪"
    
    print(f"   {sentiment_color} Sentiment detected: {sentiment}")
    
    print("\n💬 Generating reply...")
    time.sleep(1)
    
    # Generate reply based on sentiment
    if negative_count > positive_count:
        reply = f"""🙏 Thank you for sharing your honest feedback.

I understand this post may not have met your expectations. Could you help me understand what specifically you found problematic?

Constructive feedback helps me create better content for everyone. What would you suggest as an alternative approach?"""
    elif positive_count > negative_count:
        reply = f"""🙌 Thank you so much for your kind words! I'm really glad you found this post about {topic or 'this topic'} valuable.

💡 What specific aspect resonated with you the most? I'd love to hear more of your perspective!

Looking forward to more such engaging conversations! 😊"""
    elif is_question:
        reply = f"""🤔 That's a great question! Thanks for asking.

Regarding {topic or 'this topic'}, here's my perspective based on research and experience...

Would you like me to elaborate on any specific point? I'm happy to dive deeper! 💬"""
    else:
        reply = f"""👋 Thanks for engaging with this post! I appreciate you taking the time to share your thoughts on {topic or 'this topic'}.

What's your experience with this subject? I'd love to learn from your perspective as well! Feel free to share more details. 😊"""
    
    print("\n" + "=" * 70)
    print("🤖 AI SUGGESTED REPLY")
    print("=" * 70)
    print(reply)
    print("\n" + "=" * 70)
    
    # Ask to copy
    copy_choice = input("\n📋 Copy to clipboard? (y/n): ").lower()
    if copy_choice == 'y':
        try:
            import pyperclip
            pyperclip.copy(reply)
            print("✅ Copied to clipboard!")
        except ImportError:
            print("⚠️ Select the text manually and press Ctrl+C to copy.")
    
    print("\n💡 PRO TIP: Reply within 1 hour for algorithm boost!")

def optimize_resume_terminal():
    """Optimize resume with job description keywords"""
    print("\n" + "─" * 70)
    print("📄 RESUME OPTIMIZER")
    print("─" * 70)
    
    print("\n📝 Paste your resume text (press Enter twice to finish):")
    resume_lines = []
    while True:
        line = input()
        if line == "" and len(resume_lines) > 0 and resume_lines[-1] == "":
            break
        resume_lines.append(line)
    
    resume_text = "\n".join(resume_lines).strip()
    
    if not resume_text:
        print("\n❌ Please enter your resume!")
        return
    
    print("\n📋 Paste the Job Description (press Enter twice to finish):")
    jd_lines = []
    while True:
        line = input()
        if line == "" and len(jd_lines) > 0 and jd_lines[-1] == "":
            break
        jd_lines.append(line)
    
    jd_text = "\n".join(jd_lines).strip()
    
    if not jd_text:
        print("\n⚠️ No job description provided. Only adding header.")
    else:
        print("\n" + "▶" * 35)
        print("🔄 EXTRACTING KEYWORDS...")
        print("▶" * 35)
        
        time.sleep(1)
        
        # Extract keywords from JD
        skill_database = [
            "python", "java", "javascript", "react", "sql", "aws", "docker",
            "machine learning", "data science", "ai", "leadership", "communication",
            "sales", "marketing", "project management", "agile", "scrum"
        ]
        
        jd_lower = jd_text.lower()
        keywords = [skill for skill in skill_database if skill in jd_lower]
        
        print(f"\n🔍 Found {len(keywords)} keywords from Job Description:")
        if keywords:
            print(f"   🎯 {', '.join(keywords[:10])}")
            if len(keywords) > 10:
                print(f"   ... and {len(keywords) - 10} more")
    
    # Create optimized resume
    header = "═" * 70 + "\n"
    header += "📌 TARGETED KEYWORDS FOR THIS APPLICATION\n"
    header += "─" * 70 + "\n"
    if jd_text:
        header += f"🎯 Keywords: {', '.join(keywords[:15]) if keywords else 'No specific keywords found'}\n"
    header += "═" * 70 + "\n\n"
    
    optimized_resume = header + resume_text
    
    print("\n" + "=" * 70)
    print("✅ YOUR OPTIMIZED RESUME")
    print("=" * 70)
    print(optimized_resume)
    print("\n" + "=" * 70)
    
    # Ask to save
    save_choice = input("\n💾 Save to file? (y/n): ").lower()
    if save_choice == 'y':
        filename = f"optimized_resume_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(optimized_resume)
        print(f"✅ Saved to {filename}")
    
    print("\n💡 PRO TIP: Copy this resume and paste into Word, then save as PDF for submission!")

def chat_navigator_terminal():
    """Simple chat with AI Navigator"""
    print("\n" + "─" * 70)
    print("🤖 AI NAVIGATOR - Career Assistant")
    print("─" * 70)
    print("\n💡 Ask me about:")
    print("   • Companies (Google, Microsoft, Amazon, Meta, Apple)")
    print("   • Resume tips and optimization")
    print("   • Interview preparation (STAR method)")
    print("   • Networking strategies")
    print("   • Salary guides")
    print("   • Skills to learn")
    print("\n📝 Type 'exit' to return to main menu")
    print("─" * 70 + "\n")
    
    # Simple response function for terminal
    def get_simple_response(msg):
        m = msg.lower()
        
        if m in ["hi", "hello", "hey"]:
            return "👋 Hello! I'm your AI Career Navigator. How can I help you today?"
        
        if "google" in m:
            return "🏢 GOOGLE\n💰 Salary: $170K-$210K\n🎓 Intern: $8k-10k/month\n📅 Apply: Aug-Oct"
        
        if "microsoft" in m:
            return "🏢 MICROSOFT\n💰 Salary: $145K-$175K\n🎓 Intern: $7.5k-9.2k/month\n📅 Apply: Sep-Nov"
        
        if "amazon" in m:
            return "🏢 AMAZON\n💰 Salary: $155K-$175K\n🎓 Intern: $8k-9k/month"
        
        if "resume" in m:
            return "📄 RESUME TIPS\n✅ Keep 1 page\n✅ Use keywords\n✅ Quantify achievements\n✅ Action verbs"
        
        if "interview" in m:
            return "🎯 STAR METHOD\n📌 S - Situation\n📌 T - Task\n📌 A - Action\n📌 R - Result"
        
        if "help" in m:
            return "Ask me about: Google, Microsoft, Amazon, Resume, Interview, Networking, Salary"
        
        return "💡 Try asking about Google, Microsoft, Amazon, resume tips, interview prep, networking, or salary!"
    
    while True:
        user_input = input("\n💬 You: ").strip()
        
        if user_input.lower() in ['exit', 'quit', 'back', 'menu']:
            print("\n👋 Returning to main menu...")
            break
        
        if not user_input:
            continue
        
        print("\n🤖 AI Navigator: ", end="")
        time.sleep(0.5)
        response = get_simple_response(user_input)
        print(response)

def show_help():
    """Show help and tips"""
    print("\n" + "=" * 70)
    print("📚 QUICK START GUIDE")
    print("=" * 70)
    print("""
1️⃣ GENERATE LINKEDIN POST
   • Enter any topic (e.g., "AI Careers")
   • Watch 3 AI agents work together
   • Copy the post and paste on LinkedIn

2️⃣ ANALYZE COMMENTS
   • Paste any comment you received
   • AI detects sentiment (positive/negative/question)
   • Get a professional reply suggestion

3️⃣ OPTIMIZE RESUME
   • Paste your resume text
   • Paste the Job Description
   • AI extracts keywords and adds them to your resume

4️⃣ CHAT WITH AI NAVIGATOR
   • Ask any career question naturally
   • Get instant answers and advice

💡 PRO TIPS FOR LINKEDIN SUCCESS:
   • Post between 8-10 AM (Tuesday-Thursday)
   • Use 3-5 relevant hashtags
   • Reply to comments within 1 hour
   • Add images to your posts (98% more engagement)
   • Be consistent (3-4 posts per week)
""")
    print("=" * 70)

def main():
    """Main function to run the terminal application"""
    
    while True:
        clear_screen()
        print_header()
        print_menu()
        
        choice = input("\n👉 Enter your choice (1-7): ").strip()
        
        if choice == '1':
            generate_post_terminal()
            input("\n\nPress Enter to continue...")
        
        elif choice == '2':
            analyze_comment_terminal()
            input("\n\nPress Enter to continue...")
        
        elif choice == '3':
            optimize_resume_terminal()
            input("\n\nPress Enter to continue...")
        
        elif choice == '4':
            chat_navigator_terminal()
        
        elif choice == '5':
            clear_screen()
            print_header()
            print_agents_info()
            input("\nPress Enter to continue...")
        
        elif choice == '6':
            clear_screen()
            print_header()
            show_help()
            input("\nPress Enter to continue...")
        
        elif choice == '7':
            print("\n" + "=" * 70)
            print("👋 Thank you for using LinkenAI!")
            print("📧 For support, contact your AI Navigator")
            print("🚀 Keep growing on LinkedIn!")
            print("=" * 70 + "\n")
            sys.exit(0)
        
        else:
            print("\n❌ Invalid choice! Please enter 1-7.")
            time.sleep(1.5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Thanks for using LinkenAI!\n")
        sys.exit(0)