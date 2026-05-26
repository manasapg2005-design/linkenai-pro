# agents/writer_agent.py
# Mock version - No API keys required

import random
from datetime import datetime

class WriterAgent:
    def __init__(self):
        self.post_templates = [
            "🚀 Just discovered something amazing about {topic}!\n\nHere's what I learned:\n✅ {insight1}\n✅ {insight2}\n✅ {insight3}\n\nWhat's your experience with {topic}? Drop your thoughts below! 👇\n\n#LinkedIn #{topic.replace(' ', '')} #Growth",
            
            "💡 {topic} is changing the game in 2026!\n\nAfter years of observation, here's my take:\n\nThe old way ❌: Doing things manually\n\nThe new way ✅: Leveraging {topic}\n\nAre you keeping up with this trend? Let's discuss!\n\n#{topic.replace(' ', '')} #Innovation",
            
            "🎯 The truth about {topic} that nobody tells you...\n\nMost people get this wrong. Here's what actually works:\n\n1️⃣ {insight1}\n2️⃣ {insight2}\n3️⃣ {insight3}\n\nAgree? Disagree? I'd love to hear your perspective!\n\n#{topic.replace(' ', '')} #ProfessionalGrowth",
            
            "📊 3 {topic} strategies that doubled my engagement:\n\nStrategy 1: {insight1}\nStrategy 2: {insight2}\nStrategy 3: {insight3}\n\nSave this for later! 🔖\n\nWhich strategy would you try first? 👇\n\n#{topic.replace(' ', '')} #LinkedInTips"
        ]
        
        self.insights_pool = [
            "Start with a hook that grabs attention",
            "Use personal stories to build connection",
            "Add value before asking for anything",
            "Keep it concise and scannable",
            "End with a clear question to drive engagement",
            "Use bullet points for better readability",
            "Include relevant hashtags (3-5 max)",
            "Post between 8-10 AM for best reach",
            "Engage with comments within first hour",
            "Share data or research when possible",
            "Add a visual element to stop the scroll",
            "Ask open-ended questions to start conversations"
        ]
        
        self.comment_templates = [
            "Thanks for sharing! Really valuable insights on {topic}. 🙌",
            "Great post! The point about {point} really resonated with me.",
            "This is spot on! {topic} is definitely the future.",
            "Appreciate you sharing this. Quick question - how did you get started with {topic}?",
            "Brilliant breakdown! Saving this for later reference."
        ]
    
    def generate_post(self, topic, tone="professional", length="medium"):
        """
        Generate a LinkedIn post without using any API
        
        Args:
            topic (str): The topic of the post
            tone (str): professional, casual, or inspirational
            length (str): short, medium, or long
        
        Returns:
            str: Generated post content
        """
        # Randomly select 3 unique insights
        insights = random.sample(self.insights_pool, 3)
        
        # Select template based on tone
        template_index = hash(topic + tone) % len(self.post_templates)
        template = self.post_templates[template_index]
        
        # Generate the post
        post = template.format(
            topic=topic.title(),
            insight1=insights[0],
            insight2=insights[1],
            insight3=insights[2]
        )
        
        # Adjust length if needed
        if length == "short":
            post = post[:300] + "..."
        elif length == "long":
            post += "\n\n---\n\n🎓 Want to learn more? Connect with me for daily insights on {topic}!".format(topic=topic)
        
        return post
    
    def optimize_post(self, content):
        """
        Optimize an existing post for better engagement
        
        Args:
            content (str): Original post content
        
        Returns:
            dict: Optimized version with suggestions
        """
        suggestions = []
        optimized = content
        
        # Add hashtags if missing
        if "#" not in content:
            optimized += "\n\n---\n#LinkedIn #ProfessionalGrowth #CareerTips"
            suggestions.append("Added relevant hashtags")
        
        # Add question if missing
        if "?" not in content:
            optimized += "\n\n💬 What's your take on this? Share your thoughts below!"
            suggestions.append("Added engagement question")
        
        # Add emojis if missing
        if not any(emoji in content for emoji in ["🚀", "💡", "🎯", "📊"]):
            optimized = "🚀 " + optimized
            suggestions.append("Added attention-grabbing emoji")
        
        return {
            "original": content,
            "optimized": optimized,
            "suggestions": suggestions,
            "score": min(85 + len(suggestions) * 5, 100)
        }
    
    def generate_hashtags(self, topic, count=5):
        """
        Generate relevant hashtags without API
        
        Args:
            topic (str): Main topic
            count (int): Number of hashtags to generate
        
        Returns:
            list: List of hashtags
        """
        base_tags = [topic.replace(" ", ""), "LinkedIn", "Growth", "Success"]
        related_tags = {
            "marketing": ["DigitalMarketing", "ContentStrategy", "SocialMedia"],
            "ai": ["ArtificialIntelligence", "MachineLearning", "Tech"],
            "leadership": ["Management", "TeamBuilding", "Career"],
            "sales": ["BusinessGrowth", "Revenue", "ClientSuccess"],
            "career": ["JobSearch", "ProfessionalDevelopment", "Networking"]
        }
        
        hashtags = [f"#{tag}" for tag in base_tags[:count]]
        
        # Add related tags if topic matches
        topic_lower = topic.lower()
        for key, tags in related_tags.items():
            if key in topic_lower:
                additional = [f"#{tag}" for tag in tags[:count - len(hashtags)]]
                hashtags.extend(additional)
                break
        
        # Fill remaining with default tags
        default_tags = ["#Motivation", "#Inspiration", "#Success"]
        while len(hashtags) < count:
            hashtags.append(default_tags[len(hashtags) % len(default_tags)])
        
        return hashtags[:count]
    
    def get_writing_tips(self, topic=None):
        """
        Get writing tips without API
        
        Returns:
            list: Writing tips
        """
        tips = [
            "✨ Hook readers in first 2 lines",
            "📝 Use short paragraphs (2-3 lines max)",
            "🎯 Focus on one main idea per post",
            "💬 End with a specific question",
            "📅 Post consistently (3-5 times/week)",
            "🤝 Reply to every comment within 24 hours",
            "📊 Share data and real examples",
            "🔗 Tag 1-2 relevant connections (sparingly)"
        ]
        
        if topic:
            tips.append(f"🎯 For '{topic}', share personal experience first")
        
        return tips
    
    def rewrite_post(self, content, style="more_engaging"):
        """
        Rewrite a post in different style
        
        Args:
            content (str): Original content
            style (str): more_engaging, shorter, or professional
        
        Returns:
            str: Rewritten content
        """
        if style == "shorter":
            # Make it shorter
            words = content.split()
            if len(words) > 100:
                return " ".join(words[:100]) + "...\n\n👇 Full insights in comments!"
        
        elif style == "more_engaging":
            # Make it more engaging
            if "?" not in content:
                content += "\n\nWhat do YOU think? 🤔"
            if "👇" not in content and "👉" not in content:
                content = "🎯 " + content + "\n\n👇 Drop your thoughts below!"
        
        elif style == "professional":
            # Make it more professional
            content = content.replace("🚀", "").replace("💡", "").replace("🎯", "")
            content = content.replace("!", ".")
        
        return content


# Simple test if run directly
if __name__ == "__main__":
    writer = WriterAgent()
    
    print("=" * 50)
    print("Testing WriterAgent (No API Keys)")
    print("=" * 50)
    
    # Test post generation
    post = writer.generate_post("artificial intelligence", tone="professional")
    print("\n📝 Generated Post:\n")
    print(post)
    
    print("\n" + "=" * 50)
    
    # Test hashtags
    hashtags = writer.generate_hashtags("AI marketing", count=4)
    print(f"\n🏷️  Hashtags: {', '.join(hashtags)}")
    
    print("\n✅ All features working without API keys!")