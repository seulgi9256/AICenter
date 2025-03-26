
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama
from dotenv import load_dotenv

load_dotenv()

def get_llm(provider="openai", model="gpt-4o-mini", **kwargs):
    if provider =="ollama":
        return ChatOllama(
                        model=model,
                        base_url="http://localhost:11434",
                        **kwargs
                )
    else:
        return ChatOpenAI( model=model, **kwargs )