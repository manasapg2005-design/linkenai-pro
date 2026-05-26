import random
from datetime import datetime

class PosterAgent:
    """Agent: Poster Generator - Creates beautiful ASCII art posters for LinkedIn"""
    
    def __init__(self):
        self.borders = {
            "single": "─",
            "double": "═",
            "star": "✧",
            "dot": "•",
            "wave": "〜",
            "arrow": "→"
        }
        
        self.icons = {
            "tech": ["🚀", "💻", "🤖", "⚡", "🔧", "🖥️", "📱", "💡", "🎯", "🔬"],
            "career": ["💼", "🎓", "📈", "🏆", "💪", "🌟", "🎯", "📊", "🤝", "🔑"],
            "success": ["✨", "⭐", "🏆", "🎉", "💎", "🔮", "🌈", "🎨", "💫", "🔥"],
            "linkedin": ["🔗", "📝", "📢", "👥", "💬", "🤝", "📊", "🎯", "💡", "📈"]
        }
        
        self.poster_templates = {
            "tech_conference": self._generate_tech_conference,
            "career_summit": self._generate_career_summit,
            "success_story": self._generate_success_story,
            "motivational": self._generate_motivational,
            "event_announcement": self._generate_event_announcement,
            "achievement": self._generate_achievement
        }
    
    def generate_poster(self, topic, poster_type="tech_conference"):
        """Generate a poster based on topic and type"""
        poster_func = self.poster_templates.get(poster_type, self._generate_tech_conference)
        return poster_func(topic)
    
    def _generate_tech_conference(self, topic):
        """Generate a tech conference style poster"""
        current_year = datetime.now().year
        icon = random.choice(self.icons["tech"])
        
        poster = f"""
{'█' * 75}
{'▓' * 75}
{'▒' * 75}
{'░' * 75}

    ╔{'═' * 60}╗
    ║{' ' * 60}║
    ║{' ' * 18}{icon} AI MARKETING SUMMIT {current_year} {icon}{' ' * 18}║
    ║{' ' * 60}║
    ║{' ' * 12}🤖 MULTI-AGENT LINKEDIN MARKETING SYSTEM 🤖{' ' * 12}║
    ║{' ' * 60}║
    ║{' ' * 20}DEPARTMENT OF AI INNOVATION{' ' * 20}║
    ║{' ' * 22}BENGALURU, INDIA{' ' * 24}║
    ║{' ' * 60}║
    ║{'─' * 60}║
    ║{' ' * 60}║
    ║{' ' * 22}📅 DATE: {datetime.now().strftime('%d-%m-%Y')}{' ' * 27}║
    ║{' ' * 22}📍 VENUE: AI INNOVATION HUB{' ' * 26}║
    ║{' ' * 22}🎯 TOPIC: {topic[:35]}{' ' * (35 - len(topic[:35]))}{' ' * 5}║
    ║{' ' * 60}║
    ║{'─' * 60}║
    ║{' ' * 60}║
    ║{' ' * 12}⚡ LET THE AI MARKETING REVOLUTION BEGIN! ⚡{' ' * 13}║
    ║{' ' * 60}║
    ║{' ' * 8}🏆 LET THE SPIRIT OF INNOVATION AND GROWTH WIN! 🏆{' ' * 5}║
    ║{' ' * 60}║
    ║{' ' * 14}💡 CREATE • INNOVATE • AUTOMATE • DOMINATE 💡{' ' * 9}║
    ║{' ' * 60}║
    ║{' ' * 16}🎮 PLAY HARD • WORK SMART • GROW FAST 🎮{' ' * 12}║
    ║{' ' * 60}║
    ╚{'═' * 60}╝

{'░' * 75}
{'▒' * 75}
{'▓' * 75}
{'█' * 75}

    🏆 POWERED BY 5 INTELLIGENT AI AGENTS WORKING TOGETHER 🏆
    
    ┌─────────────────────────────────────────────────────────────────┐
    │  🔍 AGENT 1: RESEARCH    →  Finds trending topics & insights   │
    │  ✍️ AGENT 2: WRITER      →  Creates engaging LinkedIn posts    │
    │  🚀 AGENT 3: OPTIMIZER   →  Adds hooks, hashtags & CTAs        │
    │  💬 AGENT 4: COMMENT AI  →  Analyzes & suggests replies        │
    │  🤖 AGENT 5: CHATBOT     →  Provides career assistance         │
    └─────────────────────────────────────────────────────────────────┘

    📢 FOLLOW US FOR MORE UPDATES!
    
    #AIMarketing #{topic.replace(' ', '')[:20]} #LinkedInGrowth #MultiAgentAI
    #ContentCreator #DigitalMarketing #AIRevolution

{'=' * 75}
    🎯 READY TO TRANSFORM YOUR LINKEDIN PRESENCE? TRY NOW! 🎯
{'=' * 75}
"""
        return poster
    
    def _generate_career_summit(self, topic):
        """Generate a career summit style poster"""
        icon = random.choice(self.icons["career"])
        
        poster = f"""
╔{'═' * 70}╗
║{' ' * 70}║
║{' ' * 22}{icon} CAREER SUMMIT 2026 {icon}{' ' * 22}║
║{' ' * 70}║
║{' ' * 18}🎯 MASTER YOUR LINKEDIN PRESENCE 🎯{' ' * 18}║
║{' ' * 70}║
║{'─' * 70}║
║{' ' * 70}║
║{' ' * 25}📌 TOPIC: {topic[:40]}{' ' * (40 - len(topic[:40]))}{' ' * 5}║
║{' ' * 70}║
║{' ' * 25}📅 DATE: {datetime.now().strftime('%d %B %Y')}{' ' * 31}║
║{' ' * 25}📍 VENUE: ONLINE & HYBRID{' ' * 36}║
║{' ' * 70}║
║{'─' * 70}║
║{' ' * 70}║
║{' ' * 15}💼 WHAT YOU'LL LEARN:{' ' * 47}║
║{' ' * 70}║
║{' ' * 18}✓ AI-Powered LinkedIn Strategies{' ' * 38}║
║{' ' * 18}✓ Resume Optimization Techniques{' ' * 38}║
║{' ' * 18}✓ Interview Mastery Skills{' ' * 40}║
║{' ' * 18}✓ Networking Best Practices{' ' * 41}║
║{' ' * 70}║
║{'─' * 70}║
║{' ' * 70}║
║{' ' * 15}🎯 "The future belongs to those who prepare today"{' ' * 17}║
║{' ' * 70}║
╚{'═' * 70}╝

{'═' * 70}
    🔥 REGISTER NOW - LIMITED SEATS AVAILABLE! 🔥
    💡 Early Bird Discount Available
{'═' * 70}
"""
        return poster
    
    def _generate_success_story(self, topic):
        """Generate a success story/milestone poster"""
        icon = random.choice(self.icons["success"])
        
        poster = f"""
┌{'─' * 70}┐
│{' ' * 70}│
│{' ' * 25}{icon} SUCCESS STORY {icon}{' ' * 25}│
│{' ' * 70}│
│{' ' * 20}🏆 MILESTONE ACHIEVED! 🏆{' ' * 20}│
│{' ' * 70}│
├{'─' * 70}┤
│{' ' * 70}│
│{' ' * 20}📊 We helped professionals like you:{' ' * 30}│
│{' ' * 70}│
│{' ' * 22}✓ 10,000+ LinkedIn posts generated{' ' * 30}│
│{' ' * 22}✓ 5,000+ resumes optimized{' ' * 34}│
│{' ' * 22}✓ 3,000+ successful interviews{' ' * 33}│
│{' ' * 22}✓ 85% client satisfaction rate{' ' * 36}│
│{' ' * 70}│
├{'─' * 70}┤
│{' ' * 70}│
│{' ' * 15}🎯 "This AI system transformed my LinkedIn presence!"{' ' * 18}│
│{' ' * 22}- Satisfied Client{' ' * 44}│
│{' ' * 70}│
└{'─' * 70}┘

{'🌟' * 35}
    YOUR SUCCESS STORY COULD BE NEXT!
    🚀 Start your journey today
{'🌟' * 35}
"""
        return poster
    
    def _generate_motivational(self, topic):
        """Generate a motivational quote poster"""
        icon = random.choice(self.icons["success"])
        
        quotes = [
            "The future depends on what you do today.",
            "Success is not final, failure is not fatal.",
            "Believe you can and you're halfway there.",
            "Don't watch the clock; do what it does. Keep going.",
            "The only way to do great work is to love what you do.",
            "Your limitation—it's only your imagination.",
            "Push yourself, because no one else is going to do it for you.",
            "Great things never come from comfort zones.",
            "Dream it. Wish it. Do it.",
            "Success doesn't just find you. You have to go out and get it."
        ]
        
        quote = random.choice(quotes)
        
        poster = f"""
╔{'═' * 70}╗
║{' ' * 70}║
║{' ' * 25}{icon} DAILY MOTIVATION {icon}{' ' * 25}║
║{' ' * 70}║
║{'─' * 70}║
║{' ' * 70}║
║{' ' * 10}"{quote}"{' ' * (60 - len(quote))}║
║{' ' * 70}║
║{'─' * 70}║
║{' ' * 70}║
║{' ' * 18}🎯 Today's Topic: {topic[:40]}{' ' * (40 - len(topic[:40]))}║
║{' ' * 70}║
║{' ' * 70}║
║{' ' * 15}💪 Remember: Every expert was once a beginner.{' ' * 20}║
║{' ' * 70}║
╚{'═' * 70}╝

{'*' * 70}
    🔥 Share this motivation with your network! 🔥
    #Motivation #Success #LinkedInGrowth
{'*' * 70}
"""
        return poster
    
    def _generate_event_announcement(self, topic):
        """Generate an event announcement poster"""
        icon = random.choice(self.icons["linkedin"])
        
        poster = f"""
╭{'─' * 70}╮
│{' ' * 70}│
│{' ' * 22}{icon} ANNOUNCEMENT {icon}{' ' * 22}│
│{' ' * 70}│
│{' ' * 18}📢 NEW FEATURE LAUNCH! 📢{' ' * 18}│
│{' ' * 70}│
├{'─' * 70}┤
│{' ' * 70}│
│{' ' * 20}✨ {topic.upper()} ✨{' ' * (50 - len(topic))}│
│{' ' * 70}│
│{' ' * 70}│
│{' ' * 15}🎯 What's New:{' ' * 47}│
│{' ' * 18}• AI-Powered Resume Optimization{' ' * 37}│
│{' ' * 18}• Smart Comment Analyzer{' ' * 41}│
│{' ' * 18}• Voice Navigation Support{' ' * 40}│
│{' ' * 18}• Real-time Trend Analysis{' ' * 40}│
│{' ' * 70}│
├{'─' * 70}┤
│{' ' * 70}│
│{' ' * 15}🚀 Available Now - Try it Free!{' ' * 36}│
│{' ' * 70}│
╰{'─' * 70}╯

{'🔔' * 35}
    ✅ Update your system to access all new features!
    💡 Share your feedback with us
{'🔔' * 35}
"""
        return poster
    
    def _generate_achievement(self, topic):
        """Generate an achievement/certificate poster"""
        icon = random.choice(self.icons["success"])
        
        poster = f"""
┏{'━' * 70}┓
┃{' ' * 70}┃
┃{' ' * 25}{icon} CERTIFICATE OF ACHIEVEMENT {icon}{' ' * 25}┃
┃{' ' * 70}┃
┃{' ' * 70}┃
┃{' ' * 20}🏆 This is to certify that 🏆{' ' * 20}┃
┃{' ' * 70}┃
┃{' ' * 25}🌟 YOU 🌟{' ' * 37}┃
┃{' ' * 70}┃
┃{' ' * 15}Has successfully completed the mastery program in:{' ' * 25}┃
┃{' ' * 70}┃
┃{' ' * 25}{topic.upper()}{' ' * (45 - len(topic))}┃
┃{' ' * 70}┃
┃{' ' * 70}┃
┃{' ' * 15}📅 Date: {datetime.now().strftime('%d %B %Y')}{' ' * 35}┃
┃{' ' * 70}┃
┃{' ' * 20}🏅 Keep growing, keep learning! 🏅{' ' * 20}┃
┃{' ' * 70}┃
┗{'━' * 70}┛

{'🎉' * 35}
    SHARE YOUR ACHIEVEMENT ON LINKEDIN!
    #Achievement #Growth #Success
{'🎉' * 35}
"""
        return poster
    
    def generate_infographic(self, topic, stats):
        """Generate an infographic style poster with statistics"""
        icon = random.choice(self.icons["tech"])
        
        poster = f"""
╔{'═' * 70}╗
║{' ' * 70}║
║{' ' * 20}📊 AI MARKETING INFOGRAPHIC 📊{' ' * 20}║
║{' ' * 70}║
║{'─' * 70}║
║{' ' * 70}║
║  📈 GROWTH METRICS{' ' * 54}║
║{' ' * 70}║
║  🎯 Topic: {topic[:50]}{' ' * (50 - len(topic[:50]))}{' ' * 3}║
║{' ' * 70}║
║  📊 Engagement Rate: 94% ↑{' ' * 48}║
║  👥 Audience Reach: 50K+ {' ' * 48}║
║  💬 Comments Generated: 2.5K+{' ' * 43}║
║  🔄 Shares: 1.8K+{' ' * 51}║
║{' ' * 70}║
║{'─' * 70}║
║{' ' * 70}║
║  🔥 TOP PERFORMING TOPICS:{' ' * 49}║
║{' ' * 70}║
║  1. AI in Marketing - Engagement +312%{' ' * 38}║
║  2. Career Growth Tips - Reach +245%{' ' * 40}║
║  3. Resume Optimization - Shares +198%{' ' * 39}║
║{' ' * 70}║
║{'─' * 70}║
║{' ' * 70}║
║  💡 PRO TIP: Post between 8-10 AM for maximum reach!{' ' * 24}║
║{' ' * 70}║
╚{'═' * 70}╝

{'📊' * 35}
    Data Source: LinkedIn Analytics 2025
{'📊' * 35}
"""
        return poster
    
    def generate_festival_poster(self, topic):
        """Generate a festival/event style poster"""
        icon = random.choice(self.icons["success"])
        current_year = datetime.now().year
        
        poster = f"""
{'█' * 80}
{'▓' * 80}
{'▒' * 80}
{'░' * 80}

    ╔{'═' * 65}╗
    ║{' ' * 65}║
    ║{' ' * 20}🏆 AI MARKETING FEST {current_year} 🏆{' ' * 20}║
    ║{' ' * 65}║
    ║{' ' * 12}🤖 MULTI-AGENT LINKEDIN MARKETING SYSTEM 🤖{' ' * 12}║
    ║{' ' * 65}║
    ║{' ' * 20}🎯 THEME: {topic[:35]}{' ' * (35 - len(topic[:35]))}{' ' * 10}║
    ║{' ' * 65}║
    ║{'─' * 65}║
    ║{' ' * 65}║
    ║{' ' * 20}📅 DATE: {datetime.now().strftime('%d %B %Y')}{' ' * 26}║
    ║{' ' * 20}📍 VENUE: AI INNOVATION CENTER{' ' * 26}║
    ║{' ' * 20}🎟️ REGISTRATION: FREE / OPEN{' ' * 28}║
    ║{' ' * 65}║
    ║{'─' * 65}║
    ║{' ' * 65}║
    ║{' ' * 12}⚡ LET THE LEARNING & NETWORKING BEGIN! ⚡{' ' * 12}║
    ║{' ' * 65}║
    ║{' ' * 8}🏆 LET THE SPIRIT OF INNOVATION AND COLLABORATION WIN! 🏆{' ' * 4}║
    ║{' ' * 65}║
    ║{' ' * 14}💡 CREATE • CONNECT • COLLABORATE • CELEBRATE 💡{' ' * 8}║
    ║{' ' * 65}║
    ║{' ' * 16}🎮 LEARN • NETWORK • GROW • INSPIRE 🎮{' ' * 13}║
    ║{' ' * 65}║
    ╚{'═' * 65}╝

{'░' * 80}
{'▒' * 80}
{'▓' * 80}
{'█' * 80}

    🎉 JOIN US FOR THIS AMAZING EVENT! 🎉
    
    ┌─────────────────────────────────────────────────────────────────┐
    │  🎯 KEY HIGHLIGHTS:                                            │
    │  • Live Demos of AI Agents                                     │
    │  • Networking with Industry Experts                            │
    │  • Certificate of Participation                                │
    │  • Exclusive Resources & Templates                             │
    └─────────────────────────────────────────────────────────────────┘

    📢 REGISTER NOW - LIMITED SEATS!
    
    #AIMarketingFest #{current_year} #LinkedInGrowth #MultiAgentAI
    #Networking #CareerGrowth #Innovation

{'=' * 80}
    🎯 READY TO BOOST YOUR LINKEDIN PRESENCE? JOIN US! 🎯
{'=' * 80}
"""
        return poster

# Create singleton instance
poster_agent = PosterAgent()

# Export functions for use in app.py
def generate_poster(topic, poster_type="tech_conference"):
    """Generate a poster for the given topic"""
    return poster_agent.generate_poster(topic, poster_type)

def generate_infographic(topic, stats=None):
    """Generate an infographic poster"""
    if stats is None:
        stats = {}
    return poster_agent.generate_infographic(topic, stats)

def generate_festival_poster(topic):
    """Generate a festival style poster"""
    return poster_agent.generate_festival_poster(topic)

def get_poster_types():
    """Get available poster types"""
    return list(poster_agent.poster_templates.keys())