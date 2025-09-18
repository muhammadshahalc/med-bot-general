import os
from dotenv import load_dotenv

# Load environment variables only in development
if os.getenv("RENDER") is None:
    load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    LLM_MODEL = os.getenv("LLM_MODEL")
    LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE"))
    LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS"))
    SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT")

    @classmethod
    def validate(cls):
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is required")
