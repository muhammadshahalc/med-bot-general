import os
from dotenv import load_dotenv

# Load environment variables only in development (local)
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
        """Ensure all required env vars are set"""
        missing_vars = []
        if not cls.OPENAI_API_KEY:
            missing_vars.append("OPENAI_API_KEY")
        if not cls.LLM_MODEL:
            missing_vars.append("LLM_MODEL")
        if cls.LLM_TEMPERATURE is None:
            missing_vars.append("LLM_TEMPERATURE")
        if cls.LLM_MAX_TOKENS is None:
            missing_vars.append("LLM_MAX_TOKENS")
        if not cls.SYSTEM_PROMPT:
            missing_vars.append("SYSTEM_PROMPT")
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
