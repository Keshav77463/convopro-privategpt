from llama_index.llms.ollama import Ollama
from config.settings import Settings

# Load settings
settings = Settings()
OLLAMA_URL = settings.OLLAMA_URL

# Cache variables (to avoid reloading model again and again)
_current_model_name = None
_current_llm_instance = None


def get_ollama_llm(model_name: str):
    global _current_model_name, _current_llm_instance

    # Return cached instance if same model is requested
    if _current_model_name == model_name and _current_llm_instance is not None:
        return _current_llm_instance

    # Create new LLM instance
    llm = Ollama(
        base_url=OLLAMA_URL,
        model=model_name
    )

    # Update cache
    _current_model_name = model_name
    _current_llm_instance = llm

    return llm