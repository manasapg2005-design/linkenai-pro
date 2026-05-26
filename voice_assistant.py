# agents/voice_assistant.py
# Voice Assistant with Google Gemini API for accurate responses

import speech_recognition as sr
import pyttsx3
import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai
import warnings
warnings.filterwarnings("ignore")

# Load environment variables
load_dotenv()

class VoiceAssistant:
    def __init__(self):
        """Initialize the voice assistant with Gemini AI"""
        
        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()
        self.setup_voice()
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Setup Gemini API
        self.setup_gemini()
        
        # Assistant configuration
        self.assistant_name = "LinkedIn Assistant"
        self.is_listening = True
        self.conversation_history = []
        
        # Adjust for ambient noise
        print("🎤 Adjusting for ambient noise... Please wait")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        print("✅ Ready! Say something...")
    
    def setup_voice(self):
        """Configure voice settings"""
        voices = self.engine.getProperty('voices')
        # Try to use a female voice if available
        for voice in voices:
            if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
        
        # Set speech rate and volume
        self.engine.setProperty('rate', 180)  # Words per minute
        self.engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
    
    def setup_gemini(self):
        """Configure Google Gemini API"""
        # Get API key from environment variable
        self.api_key = os.getenv('GEMINI_API_KEY')
        
        if not self.api_key:
            print("⚠️ WARNING: GEMINI_API_KEY not found in environment variables!")
            print("Please set your API key:")
            print("1. Get your key from: https://aistudio.google.com/")
            print("2. Create a .env file with: GEMINI_API_KEY=your_key_here")
            self.use_mock_mode = True
            print("🔄 Running in MOCK MODE (limited responses)")
        else:
            try:
                # Configure Gemini
                genai.configure(api_key=self.api_key)
                
                # Use the flash model for faster responses
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Test the API
                test_response = self.model.generate_content("Test connection")
                if test_response.text:
                    print("✅ Gemini API connected successfully!")
                    self.use_mock_mode = False
                else:
                    raise Exception("Empty response from API")
                    
            except Exception as e:
                print(f"⚠️ Gemini API Error: {str(e)}")
                print("🔄 Falling back to MOCK MODE")
                self.use_mock_mode = True
    
    def listen(self, timeout=5, phrase_time_limit=10):
        """
        Listen for voice input from microphone
        
        Args:
            timeout: Maximum seconds to wait for speech to start
            phrase_time_limit: Maximum seconds for the phrase
        
        Returns:
            str: Recognized text or None if failed
        """
        try:
            print("\n🎧 Listening...")
            with self.microphone as source:
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout, 
                    phrase_time_limit=phrase_time_limit
                )
            
            print("🔄 Processing speech...")
            text = self.recognizer.recognize_google(audio)
            print(f"📝 You said: {text}")
            return text.lower()
            
        except sr.WaitTimeoutError:
            print("⏰ No speech detected within timeout period")
            return None
        except sr.UnknownValueError:
            print("❓ Could not understand the audio")
            return None
        except sr.RequestError as e:
            print(f"⚠️ Speech recognition service error: {e}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return None
    
    def speak(self, text):
        """
        Convert text to speech
        
        Args:
            text: Text to speak
        """
        try:
            print(f"🤖 Assistant: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"⚠️ Text-to-speech error: {e}")
            print(f"💬 (Would have said): {text}")
    
    def get_ai_response(self, user_input):
        """
        Get response from Gemini AI or fallback to mock responses
        
        Args:
            user_input: User's spoken text
        
        Returns:
            str: AI generated response
        """
        # Add context about LinkedIn
        system_prompt = """You are a helpful LinkedIn AI assistant. Your role is to help users with:
- Creating engaging LinkedIn posts
- Improving their LinkedIn profile
- Growing their professional network
- Getting more engagement on posts
- Understanding LinkedIn best practices
- Career advice and professional development

Keep responses concise, actionable, and friendly. Use emojis occasionally but don't overdo it.
If asked about something unrelated to LinkedIn/professional growth, politely redirect to your expertise.

Remember: Be helpful, professional, and engaging!"""
        
        if not self.use_mock_mode:
            try:
                # Prepare conversation context
                conversation = f"{system_prompt}\n\nUser: {user_input}\nAssistant:"
                
                # Get response from Gemini
                response = self.model.generate_content(conversation)
                
                if response and response.text:
                    # Store in conversation history
                    self.conversation_history.append({
                        "user": user_input,
                        "assistant": response.text,
                        "source": "gemini"
                    })
                    return response.text
                else:
                    raise Exception("Empty response from Gemini")
                    
            except Exception as e:
                print(f"⚠️ Gemini API error: {e}")
                print("🔄 Using mock response instead")
                return self.get_mock_response(user_input)
        else:
            return self.get_mock_response(user_input)
    
    def get_mock_response(self, user_input):
        """
        Fallback mock responses when Gemini is unavailable
        
        Args:
            user_input: User's spoken text
        
        Returns:
            str: Mock response
        """
        user_input_lower = user_input.lower()
        
        # Post writing related
        if any(word in user_input_lower for word in ['write', 'post', 'create', 'generate']):
            return "I can help you write a great LinkedIn post! What topic would you like to write about? For example, you could share a career lesson, industry insight, or personal achievement."
        
        # Engagement related
        elif any(word in user_input_lower for word in ['engagement', 'like', 'comment', 'reach']):
            return "To boost engagement on LinkedIn, try posting questions that encourage discussion, share personal stories, and always respond to comments within the first hour. Would you like specific tips for your industry?"
        
        # Hashtag related
        elif any(word in user_input_lower for word in ['hashtag', '#', 'tag']):
            return "For best results on LinkedIn, use 3-5 relevant hashtags per post. Mix popular ones like #LinkedIn with niche-specific tags. I can suggest hashtags for your topic if you tell me what you're posting about!"
        
        # Best time to post
        elif any(word in user_input_lower for word in ['when', 'time', 'schedule', 'best time']):
            return "The best times to post on LinkedIn are Tuesday through Thursday, between 8-10 AM and 12-1 PM in your target audience's timezone. Weekends typically have lower engagement unless you're in a B2C industry."
        
        # Profile optimization
        elif any(word in user_input_lower for word in ['profile', 'optimize', 'headline', 'photo']):
            return "To optimize your LinkedIn profile: use a professional headshot, write a compelling headline (not just your job title), add a background banner that showcases your brand, and fill out the 'About' section with your value proposition."
        
        # Growth related
        elif any(word in user_input_lower for word in ['grow', 'followers', 'network', 'connect']):
            return "The best way to grow on LinkedIn is to engage genuinely with others in your industry. Comment on posts from thought leaders, share valuable insights, and connect with people you've actually interacted with. Quality over quantity!"
        
        # Greetings
        elif any(word in user_input_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            return "Hello! I'm your LinkedIn AI assistant. How can I help you with your professional presence today?"
        
        # Help
        elif 'help' in user_input_lower:
            return "I can help you with: writing LinkedIn posts, optimizing your profile, increasing engagement, finding the best posting times, suggesting hashtags, and growing your network. What would you like assistance with?"
        
        # Goodbye
        elif any(word in user_input_lower for word in ['bye', 'goodbye', 'exit', 'quit', 'stop']):
            return "Goodbye! Remember to post consistently and engage with your network. Come back anytime you need help with your LinkedIn strategy!"
        
        # Default response
        else:
            responses = [
                f"That's interesting! Could you tell me more about how that relates to your LinkedIn or professional goals?",
                f"I see! As a LinkedIn assistant, I specialize in helping with professional content and networking. How can I assist with your LinkedIn presence?",
                f"Thanks for sharing! Would you like help turning that into a LinkedIn post or getting advice on how to share it professionally?",
                f"I'm here to help with your LinkedIn strategy. Would you like some tips on posting, engagement, or profile optimization?"
            ]
            import random
            return random.choice(responses)
    
    def process_command(self, user_input):
        """
        Process voice commands for specific actions
        
        Args:
            user_input: User's spoken text
        
        Returns:
            bool: True if should continue listening, False to exit
        """
        user_input_lower = user_input.lower()
        
        # Exit commands
        if any(word in user_input_lower for word in ['exit', 'quit', 'stop', 'goodbye', 'bye']):
            self.speak("Goodbye! Keep growing your professional network!")
            return False
        
        # Get AI response for everything else
        response = self.get_ai_response(user_input)
        self.speak(response)
        
        return True
    
    def start(self):
        """Start the voice assistant"""
        self.speak(f"Hello! I'm your {self.assistant_name}. How can I help you with LinkedIn today?")
        
        while self.is_listening:
            user_input = self.listen()
            
            if user_input:
                # Check for exit commands
                if any(word in user_input for word in ['exit', 'quit', 'goodbye', 'bye', 'stop']):
                    self.speak("Goodbye! Keep growing your professional network!")
                    break
                
                # Process the command
                response = self.get_ai_response(user_input)
                self.speak(response)
            else:
                # No input detected
                print("No input detected. Say something or say 'exit' to quit.")
    
    def run_text_mode(self):
        """Run assistant in text-only mode (no microphone)"""
        print("\n📝 Text Mode Started")
        print("Type your questions (type 'exit' to quit):")
        print("-" * 50)
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if user_input.lower() in ['exit', 'quit', 'bye', 'goodbye']:
                    print("Assistant: Goodbye! Keep growing your professional network!")
                    break
                
                if user_input:
                    response = self.get_ai_response(user_input)
                    print(f"Assistant: {response}")
                else:
                    print("Assistant: Please type a question or command.")
                    
            except KeyboardInterrupt:
                print("\n\nAssistant: Goodbye!")
                break
            except Exception as e:
                print(f"Assistant: Sorry, an error occurred: {e}")
    
    def test_microphone(self):
        """Test if microphone is working"""
        print("\n🎤 Testing microphone...")
        try:
            with self.microphone as source:
                print("Please say something...")
                audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=3)
                text = self.recognizer.recognize_google(audio)
                print(f"✅ Microphone working! Detected: '{text}'")
                return True
        except Exception as e:
            print(f"❌ Microphone test failed: {e}")
            return False


# Main execution
if __name__ == "__main__":
    print("=" * 60)
    print("🎙️  LinkedIn AI Voice Assistant")
    print("=" * 60)
    print("\nThis assistant uses Google Gemini API for intelligent responses.")
    print("Make sure you have set your GEMINI_API_KEY in .env file\n")
    
    assistant = VoiceAssistant()
    
    # Choose mode
    print("\nChoose mode:")
    print("1. Voice Mode (speak to the assistant)")
    print("2. Text Mode (type your questions)")
    print("3. Test Microphone only")
    
    choice = input("\nEnter choice (1/2/3): ").strip()
    
    if choice == "1":
        assistant.start()
    elif choice == "2":
        assistant.run_text_mode()
    elif choice == "3":
        assistant.test_microphone()
    else:
        print("Invalid choice. Starting in Voice Mode...")
        assistant.start()