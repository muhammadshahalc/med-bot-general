from langchain_openai import ChatOpenAI
from .config import Config

def create_llm():
    """Create and return a ChatOpenAI instance"""
    Config.validate()
    return ChatOpenAI(
        model=Config.LLM_MODEL,
        temperature=Config.LLM_TEMPERATURE,
        max_tokens=Config.LLM_MAX_TOKENS,
        openai_api_key=Config.OPENAI_API_KEY
    )
