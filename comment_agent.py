import re
import random
from datetime import datetime

class CommentAgent:
    """Agent 4: Comment AI - Analyzes comments and suggests professional replies"""
    
    def __init__(self):
        # Sentiment keywords
        self.positive_keywords = [
            "great", "good", "awesome", "amazing", "excellent", "helpful", "insightful",
            "love", "thank", "appreciate", "useful", "valuable", "brilliant", "fantastic",
            "superb", "wonderful", "impressive", "perfect", "nice", "cool", "best",
            "like this", "agree", "well said", "spot on", "informative", "thanks",
            "appreciated", "wonderful", "outstanding", "remarkable", "incredible"
        ]
        
        self.negative_keywords = [
            "bad", "wrong", "useless", "hate", "terrible", "awful", "disappointed",
            "worst", "poor", "waste", "misleading", "false", "incorrect", "stupid",
            "ridiculous", "horrible", "sucks", "pathetic", "annoying", "garbage",
            "trash", "shit", "fuck", "damn", "crap", "bullshit", "nonsense"
        ]
        
        # Question indicators
        self.question_words = ["?", "how", "what", "why", "when", "which", "where", "who", "could", "would", "should"]
        
        # Reply templates based on sentiment
        self.reply_templates = {
            "positive": [
                "🙌 Thank you so much for your kind words! I'm really glad you found this post valuable. 😊\n\nWhat specific aspect resonated with you the most? I'd love to hear your thoughts!",
                "Thank you for your wonderful feedback! 🙏\n\nYour encouragement means a lot. What other topics would you like me to cover? 💡",
                "I truly appreciate your thoughtful comment! 🌟\n\nIt's readers like you who make this community special. Feel free to share your experience as well! 💬",
                "Thanks a ton for your support! 🙌\n\nI'm curious - what's your biggest takeaway from this post? Would love to continue this conversation! 🤝"
            ],
            "negative": [
                "Thank you for sharing your honest feedback, even though it's critical. 🙏\n\nI understand this post may not have met your expectations. Could you help me understand what specifically you found problematic?",
                "I appreciate your perspective, even though it differs from mine. 💭\n\nConstructive feedback helps me create better content. What would you suggest as an alternative approach?",
                "Thanks for being honest. 👋\n\nI'm always looking to improve. Could you share more details about what you disagree with? Your input is valuable.",
                "I respect your opinion, even if we see things differently. 🤔\n\nLet's have a constructive discussion - what would you add to make this better?"
            ],
            "question": [
                "That's a great question! 🤔\n\nLet me share my perspective based on research and experience...\n\nWould you like me to elaborate on any specific aspect? I'm happy to dive deeper! 💬",
                "Excellent question! 🎯\n\nHere's what I've learned about this topic...\n\nIs there a particular area you'd like me to focus on?",
                "I love this question! 💡\n\nFrom my experience, here's what works...\n\nDo you have a specific situation in mind? I'd love to give more tailored advice."
            ],
            "neutral": [
                "Thanks for engaging with this post! 👋\n\nI appreciate you taking the time to share your thoughts. What's your experience with this topic? I'd love to learn from your perspective as well! 😊",
                "Thank you for your comment! 🙏\n\nI'm always excited to hear different viewpoints. What specifically caught your attention in this post? 💭",
                "Appreciate you joining the conversation! 🤝\n\nYour input helps make this community richer. Feel free to share more details - the best discussions happen when we exchange ideas!"
            ]
        }
        
        # Professional closing lines
        self.closing_lines = [
            "\n\n💡 **Pro Tip:** Engaging with comments within 1 hour boosts your post reach significantly!",
            "\n\n📌 **Remember:** Authentic engagement builds stronger professional relationships.",
            "\n\n🎯 **Quick Tip:** Follow up with a DM to turn this conversation into a meaningful connection.",
            "\n\n💬 **Let's keep the conversation going!** What other topics interest you?",
            "\n\n🤝 **Want to continue this discussion?** Feel free to DM me for deeper insights!"
        ]
        
        # Time-based greetings
        self.time_greetings = {
            "morning": "Good morning! ☀️",
            "afternoon": "Good afternoon! 🌤️",
            "evening": "Good evening! 🌙",
            "night": "Hello there! ✨"
        }
    
    def get_time_greeting(self):
        """Get time-appropriate greeting"""
        current_hour = datetime.now().hour
        
        if 5 <= current_hour < 12:
            return self.time_greetings["morning"]
        elif 12 <= current_hour < 17:
            return self.time_greetings["afternoon"]
        elif 17 <= current_hour < 22:
            return self.time_greetings["evening"]
        else:
            return self.time_greetings["night"]
    
    def detect_sentiment(self, comment):
        """Detect sentiment of the comment (positive, negative, neutral, question)"""
        comment_lower = comment.lower()
        
        # Check for strong negative words first
        for word in self.negative_keywords:
            if word in comment_lower:
                return "negative"
        
        # Check if it's a question
        is_question = any(word in comment_lower for word in self.question_words) or "?" in comment
        
        # Count positive and negative words
        positive_count = sum(1 for word in self.positive_keywords if word in comment_lower)
        negative_count = sum(1 for word in self.negative_keywords if word in comment_lower)
        
        if is_question and positive_count == 0 and negative_count == 0:
            return "question"
        elif positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"
    
    def extract_topics(self, comment):
        """Extract potential topics from comment"""
        topics = []
        
        # Common topic keywords
        topic_keywords = {
            "resume": ["resume", "cv", "curriculum", "application"],
            "interview": ["interview", "prep", "star", "behavioral", "technical"],
            "networking": ["network", "connect", "linkedin", "connection", "dm"],
            "salary": ["salary", "pay", "compensation", "package", "ctc"],
            "skills": ["skill", "learn", "course", "certification", "training"],
            "job": ["job", "internship", "position", "role", "opening", "hiring"],
            "company": ["google", "microsoft", "amazon", "meta", "apple", "facebook"]
        }
        
        comment_lower = comment.lower()
        for topic, keywords in topic_keywords.items():
            for keyword in keywords:
                if keyword in comment_lower:
                    topics.append(topic)
                    break
        
        return list(set(topics))  # Remove duplicates
    
    def generate_reply(self, comment, post_topic=""):
        """Generate a professional reply based on comment sentiment"""
        
        sentiment = self.detect_sentiment(comment)
        topics = self.extract_topics(comment)
        time_greeting = self.get_time_greeting()
        
        # Choose appropriate template
        templates = self.reply_templates.get(sentiment, self.reply_templates["neutral"])
        reply = random.choice(templates)
        
        # Add time greeting if appropriate
        if "morning" in time_greeting or "afternoon" in time_greeting:
            reply = f"{time_greeting}\n\n{reply}"
        
        # Add topic-specific context if available
        if topics:
            topic_context = f"\n\n💡 **Regarding {'/'.join(topics)}:** I'd be happy to share more resources if you're interested!"
            reply += topic_context
        
        # Add closing line
        closing = random.choice(self.closing_lines)
        reply += closing
        
        # If comment contains a specific question, add extra engagement
        if "?" in comment:
            reply += "\n\n❓ **Quick follow-up:** Would you like me to go deeper into any specific area?"
        
        return reply
    
    def analyze_comment(self, comment):
        """Provide full analysis of a comment including sentiment and suggested actions"""
        
        sentiment = self.detect_sentiment(comment)
        topics = self.extract_topics(comment)
        reply = self.generate_reply(comment)
        
        # Sentiment icons
        sentiment_icons = {
            "positive": "😊 Positive",
            "negative": "😠 Negative",
            "question": "🤔 Question",
            "neutral": "😐 Neutral"
        }
        
        # Action suggestions based on sentiment
        action_suggestions = {
            "positive": "✅ Engage quickly (within 30 minutes) → Builds loyalty\n✅ Ask a follow-up question\n✅ Consider sending a DM to connect",
            "negative": "⚠️ Respond professionally within 1-2 hours\n✅ Don't take it personally\n✅ Ask for specific feedback\n✅ Offer to discuss further via DM",
            "question": "🎯 Answer thoroughly (within 1 hour)\n✅ Provide examples or resources\n✅ Ask if they need clarification\n✅ Follow up to ensure satisfaction",
            "neutral": "💬 Keep the conversation going\n✅ Ask for their experience\n✅ Share additional insights\n✅ Encourage deeper discussion"
        }
        
        analysis = f"""
📊 **COMMENT ANALYSIS**

**Original Comment:** "{comment}"

**Detected Sentiment:** {sentiment_icons.get(sentiment, "😐 Neutral")}

**Identified Topics:** {', '.join(topics) if topics else 'General discussion'}

**🤖 AI Suggested Reply:**
{reply}

**📌 Recommended Actions:**
{action_suggestions.get(sentiment, action_suggestions["neutral"])}

---
💡 **Pro Tip:** Responding within the first hour of a comment significantly increases post engagement!
"""
        
        return analysis
    
    def generate_bulk_replies(self, comments, post_topic=""):
        """Generate replies for multiple comments at once"""
        replies = []
        
        for comment in comments:
            reply = self.generate_reply(comment, post_topic)
            replies.append({
                "original": comment,
                "reply": reply,
                "sentiment": self.detect_sentiment(comment)
            })
        
        return replies
    
    def get_reply_statistics(self, comments):
        """Get statistics about comments for analytics"""
        sentiments = {"positive": 0, "negative": 0, "neutral": 0, "question": 0}
        
        for comment in comments:
            sentiment = self.detect_sentiment(comment)
            sentiments[sentiment] = sentiments.get(sentiment, 0) + 1
        
        total = len(comments)
        stats = {
            "total": total,
            "positive_percentage": round((sentiments["positive"] / total) * 100, 1) if total > 0 else 0,
            "negative_percentage": round((sentiments["negative"] / total) * 100, 1) if total > 0 else 0,
            "neutral_percentage": round((sentiments["neutral"] / total) * 100, 1) if total > 0 else 0,
            "question_percentage": round((sentiments["question"] / total) * 100, 1) if total > 0 else 0,
            "sentiments": sentiments
        }
        
        return stats
    
    def should_respond(self, comment):
        """Determine if a comment should get a response"""
        # Always respond to comments with questions or positive/negative sentiment
        sentiment = self.detect_sentiment(comment)
        
        # Always respond to questions and negative comments
        if sentiment == "question" or sentiment == "negative":
            return True
        
        # Respond to positive comments 90% of the time
        if sentiment == "positive":
            return random.random() < 0.9
        
        # Respond to neutral comments 60% of the time
        return random.random() < 0.6

# Create singleton instance
comment_agent = CommentAgent()

# Export functions for use in app.py
def analyze_comment(comment, topic=""):
    """Main function to analyze a comment"""
    return comment_agent.analyze_comment(comment)

def generate_reply(comment, topic=""):
    """Main function to generate a reply for a comment"""
    return comment_agent.generate_reply(comment, topic)

def get_comment_sentiment(comment):
    """Get sentiment of a comment"""
    return comment_agent.detect_sentiment(comment)

def bulk_generate_replies(comments, topic=""):
    """Generate replies for multiple comments"""
    return comment_agent.generate_bulk_replies(comments, topic)