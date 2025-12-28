from groq import Groq
from utils.config import Config

client = Groq(api_key=Config.GROQ_API_KEY)

try:
    models = client.models.list()
    print("Available Groq models:")
    for model in models.data:
        print(f"- {model.id}")
except Exception as e:
    print(f"Error: {e}")