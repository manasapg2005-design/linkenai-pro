# agents/chatbot_agent.py
# LinkedIn AI Chatbot - No API keys required

import random
from datetime import datetime

class ChatbotAgent:
    def __init__(self):
        self.conversation_history = []
        
        # Intent patterns (simple keyword matching)
        self.intent_patterns = {
            "greeting": ["hello", "hi", "hey", "greetings", "sup", "good morning", "good afternoon"],
            "post_writing": ["write", "post", "content", "create post", "generate post", "make a post"],
            "engagement": ["engagement", "likes", "comments", "reach", "impressions", "views"],
            "best_time": ["when to post", "best time", "schedule", "optimal time"],
            "hashtags": ["hashtag", "#", "tags", "trending topics"],
            "growth": ["grow", "followers", "increase", "audience", "network"],
            "analytics": ["analytics", "performance", "metrics", "stats", "insights"],
            "optimization": ["optimize", "improve", "better", "tips", "advice"],
            "trends": ["trend", "viral", "popular", "hot topic"],
            "help": ["help", "support", "what can you do", "capabilities"],
            "goodbye": ["bye", "goodbye", "see you", "exit", "quit"],
            "thanks": ["thanks", "thank you", "appreciate", "grateful"]
        }
        
        # Response templates by intent
        self.responses = {
            "greeting": [
                "Hello! 👋 I'm your LinkedIn AI assistant. How can I help with your content today?",
                "Hey there! 🚀 Ready to create some amazing LinkedIn content?",
                "Hi! 👋 What would you like to work on today? Posts, engagement, or strategy?",
                "Greetings! 📝 I'm here to help you grow on LinkedIn. Ask me anything!"
            ],
            "post_writing": [
                "I'd love to help you write a post! 🎯 What topic would you like to cover?",
                "Great! Let's create an engaging post. What's the main message you want to share?",
                "Post creation coming right up! 📝 Tell me your topic and I'll generate ideas.",
                "Ready to write! 💡 Share your topic or key points, and I'll help craft the perfect post."
            ],
            "engagement": [
                "To boost engagement, try these tactics:\n✅ Post questions that spark discussion\n✅ Reply to comments within 1 hour\n✅ Use 3-5 relevant hashtags\n✅ Share personal stories\nWhat would you like to focus on?",
                "Engagement tip: Start with a bold statement, then ask 'What's your experience?' This drives comments! 💬",
                "The best engagement strategy? Consistency plus value. Post 3-5x weekly and always reply to comments! 🚀"
            ],
            "best_time": [
                "Best times to post on LinkedIn:\n📅 Tuesday-Thursday\n⏰ 8-10 AM or 12-1 PM (local time)\n📊 Test different times to find YOUR audience peak!",
                "Based on data, post between 8-10 AM Tuesday-Thursday for maximum reach. But your industry may vary! 📈"
            ],
            "hashtags": [
                "Hashtag tips:\n🏷️ Use 3-5 maximum\n🏷️ Mix popular (500K+) and niche (10K-50K)\n🏷️ Create a branded hashtag\nWant me to generate hashtags for your topic?",
                "Top hashtags for 2026: #LinkedIn #Growth #Career #Innovation #Leadership #Marketing. Which niche are you in? 🎯"
            ],
            "growth": [
                "To grow on LinkedIn:\n📈 Post consistently (3-5x/week)\n🤝 Engage with 10+ people daily\n💬 Comment meaningfully on industry leaders' posts\n📝 Share your journey, not just wins\nNeed a growth plan?",
                "The fastest way to grow? Add value first, ask for nothing. Share insights, celebrate others, and be authentic! 🌱"
            ],
            "analytics": [
                "Key metrics to track:\n👁️ Impressions - Your reach\n❤️ Engagement rate - Likes + comments + shares\n📊 Click-through rate - Link clicks\n💬 Comment-to-like ratio\nWant tips to improve any metric?",
                "Check your post analytics weekly. Look for patterns in what works and double down! 📊"
            ],
            "optimization": [
                "To optimize your posts:\n✨ First 2 lines must hook readers\n📝 Use short paragraphs (2-3 lines)\n🎯 Add a clear CTA (question or action)\n🖼️ Include an image or carousel\nWant me to review a post?",
                "Optimization tip: Your post should be 1200-1500 characters for best engagement. Not too short, not too long! ✂️"
            ],
            "trends": [
                "Current LinkedIn trends:\n🔥 Short video content\n🔥 Carousel posts (document-style)\n🔥 Employee advocacy\n🔥 Personal stories over company news\nWant to create trending content?",
                "To spot trends, follow LinkedIn's 'Today's News' and industry hashtags. Stay ahead! 🎯"
            ],
            "help": [
                "I can help you with:\n✍️ Writing LinkedIn posts\n📊 Engagement strategies\n🏷️ Hashtag recommendations\n📅 Best posting times\n📈 Growth tactics\n🔧 Post optimization\nWhat would you like help with?",
                "My capabilities:\n- Generate posts from topics\n- Optimize existing content\n- Suggest hashtags\n- Share engagement tips\n- Answer LinkedIn questions\nJust ask! 🚀"
            ],
            "goodbye": [
                "Goodbye! 👋 Come back when you need help with LinkedIn content!",
                "See you later! 🚀 Keep creating amazing content!",
                "Bye! Remember - consistency wins on LinkedIn. You've got this! 💪"
            ],
            "thanks": [
                "You're very welcome! 🙌 Happy to help. Anything else you need?",
                "My pleasure! 🎯 Let me know if you have more questions.",
                "Anytime! 🤝 That's what I'm here for. What's next?"
            ],
            "default": [
                "Interesting! 🤔 Could you tell me more? Or would you like help with posts, engagement, or growth?",
                "I see! 🎯 How about I help you write a post or optimize your LinkedIn strategy?",
                "Thanks for sharing! 💬 Would you like some LinkedIn tips for that topic?",
                "Got it! 📝 What specific LinkedIn help do you need - content creation, analytics, or growth?"
            ]
        }
        
        self.follow_ups = {
            "post_writing": "What topic would you like to write about?",
            "hashtags": "What industry or topic are you targeting?",
            "optimization": "Could you share your post for me to review?",
            "growth": "What's your current follower count and engagement rate?"
        }
    
    def respond(self, message):
        """Generate a response based on user message"""
        # Store user message
        self.conversation_history.append({
            "user": message,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        # Clean and analyze message
        clean_msg = message.lower().strip()
        
        # Detect intent
        intent = self._detect_intent(clean_msg)
        
        # Generate response
        response = self._generate_response(intent, clean_msg)
        
        # Add follow-up if appropriate
        if intent in self.follow_ups and "?" not in response:
            response += f"\n\n{self.follow_ups[intent]}"
        
        # Store bot response
        self.conversation_history.append({
            "bot": response,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        return response
    
    def _detect_intent(self, message):
        """Detect intent from user message"""
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if pattern in message:
                    return intent
        return "default"
    
    def _generate_response(self, intent, message):
        """Generate response based on intent"""
        response_list = self.responses.get(intent, self.responses["default"])
        response = random.choice(response_list)
        
        # Personalize based on message context
        if "post" in message and "write" in message:
            return "Let's write an amazing post! 🎯 What's your topic?"
        
        if "hashtag" in message or "#" in message:
            return "Generated hashtags for you! 🏷️ Try: #LinkedIn #Growth #[YourTopic] #Success\n\nWhat's your specific topic for more targeted hashtags?"
        
        if "tip" in message or "advice" in message:
            return "📝 Quick tip: Always end your posts with a question. It doubles engagement!\n\nWant more specific advice?"
        
        return response
    
    def get_conversation_summary(self):
        """Get summary of conversation history"""
        if not self.conversation_history:
            return "No conversation yet. Start chatting with me!"
        
        user_messages = [h["user"] for h in self.conversation_history if "user" in h]
        return {
            "total_exchanges": len(user_messages),
            "last_message": self.conversation_history[-1] if self.conversation_history else None,
            "topics_discussed": list(set(self._detect_intent(msg) for msg in user_messages if msg))
        }
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        return "Conversation history cleared! Ready to start fresh. 👋"
    
    def get_suggested_questions(self):
        """Get suggested questions for users"""
        return [
            "💬 Can you help me write a LinkedIn post?",
            "📊 How do I get more engagement?",
            "⏰ What's the best time to post?",
            "🏷️ Generate hashtags for marketing",
            "📈 How can I grow my followers?",
            "🔧 Optimize my LinkedIn post",
            "📅 How often should I post?",
            "🎯 What topics are trending?"
        ]


# Run directly to test
if __name__ == "__main__":
    chatbot = ChatbotAgent()
    
    print("=" * 60)
    print("🤖 LINKEDIN AI CHATBOT (No API Keys Required)")
    print("=" * 60)
    print("\nType 'quit' to exit, 'clear' to reset history, 'suggest' for ideas\n")
    
    while True:
        user_input = input("\n👤 You: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("🤖 Bot: Goodbye! 👋 Keep crushing it on LinkedIn!")
            break
        elif user_input.lower() == 'clear':
            print(f"🤖 Bot: {chatbot.clear_history()}")
        elif user_input.lower() == 'suggest':
            print("🤖 Suggested questions:")
            for q in chatbot.get_suggested_questions():
                print(f"   {q}")
        elif user_input:
            response = chatbot.respond(user_input)
            print(f"🤖 Bot: {response}")