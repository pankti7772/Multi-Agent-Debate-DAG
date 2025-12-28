import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration management"""
    
    # API Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    # Model Configuration
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    
    # Debate Configuration
    MAX_ROUNDS = int(os.getenv("MAX_ROUNDS", "8"))
    AGENT_A_PERSONA = os.getenv("AGENT_A_PERSONA", "Scientist")
    AGENT_B_PERSONA = os.getenv("AGENT_B_PERSONA", "Philosopher")
    
    # Runtime Configuration
    SEED = None
    LOG_PATH = "logs/debate_log.jsonl"
    TOPIC = "Is AI sentient?"

    @classmethod
    def update(cls, **kwargs):
        """Update config dynamically (e.g. from CLI args)"""
        for key, value in kwargs.items():
            if hasattr(cls, key):
                setattr(cls, key, value)