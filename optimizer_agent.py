import random

class OptimizerAgent:
    """Agent 3: Optimizer Agent - Adds hooks, hashtags, and CTAs"""
    
    def __init__(self):
        self.hooks = [
            "🔥 STOP SCROLLING! This changes everything!",
            "💡 3 things nobody tells you about this:",
            "🚀 If you ignore this, you'll fall behind:",
            "🎯 The truth that most people miss:",
            "⚡ This will change your perspective:",
            "📢 ATTENTION: This is not common knowledge:",
            "💭 I wish someone told me this earlier:",
            "🔑 The #1 secret most professionals ignore:"
        ]
        
        self.ctas = [
            "👇 Drop a '💡' if this helped you!",
            "💬 What's your experience? Comment below!",
            "♻️ Repost to help your network grow!",
            "🔔 Follow me for more such insights!",
            "💭 Tag a friend who needs to see this!",
            "📌 Save this post for later reference!",
            "✍️ Share your thoughts in the comments!",
            "🤝 Connect with me for daily insights!"
        ]
        
        self.hashtag_pools = {
            "growth": ["#LinkedInGrowth", "#CareerAdvice", "#ProfessionalDevelopment", "#PersonalBranding"],
            "tech": ["#AI", "#MachineLearning", "#TechCareers", "#FutureOfWork", "#DigitalTransformation"],
            "students": ["#StudentSuccess", "#InternshipTips", "#CollegeLife", "#Freshers", "#CampusToCorporate"],
            "startup": ["#Startup", "#Entrepreneurship", "#BusinessGrowth", "#VentureCapital", "#Founder"],
            "engagement": ["#Networking", "#LinkedInTips", "#ContentCreator", "#ViralPost", "#Engagement"]
        }
    
    def optimize(self, post):
        """Add hooks, hashtags, and CTAs to the post"""
        
        # Select random hook and CTA
        hook = random.choice(self.hooks)
        cta = random.choice(self.ctas)
        
        # Select hashtags based on post content
        selected_hashtags = []
        post_lower = post.lower()
        
        if "student" in post_lower or "internship" in post_lower:
            selected_hashtags.extend(self.hashtag_pools["students"])
        if "startup" in post_lower or "entrepreneur" in post_lower:
            selected_hashtags.extend(self.hashtag_pools["startup"])
        if "ai" in post_lower or "tech" in post_lower:
            selected_hashtags.extend(self.hashtag_pools["tech"])
        
        selected_hashtags.extend(self.hashtag_pools["growth"])
        selected_hashtags.extend(self.hashtag_pools["engagement"])
        
        # Remove duplicates and select 7 random hashtags
        unique_hashtags = list(set(selected_hashtags))
        final_hashtags = random.sample(unique_hashtags, min(7, len(unique_hashtags)))
        hashtag_str = " ".join(final_hashtags)
        
        # Add time-based greeting for replies
        from datetime import datetime
        current_hour = datetime.now().hour
        if current_hour < 12:
            time_greeting = "Good morning"
        elif current_hour < 17:
            time_greeting = "Good afternoon"
        else:
            time_greeting = "Good evening"
        
        # Build optimized post
        optimized = f"""{hook}

{post}

---

{cta}

{hashtag_str}

---
💬 **Quick Reply Tip:** When someone comments, try: "{time_greeting}! Thanks for engaging! What specific part resonated with you? 💭"
"""
        
        return optimized

optimizer_agent = OptimizerAgent()

def optimize_post(post):
    return optimizer_agent.optimize(post)