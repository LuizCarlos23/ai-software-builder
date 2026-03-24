from pathlib import Path

class Config:
    # Modelos
    ARCHITECT_MODEL = "llama3.2"
    CODER_MODEL = "phi3"
    REVIEWER_MODEL = "llama3.2"
    
    # URLs
    OLLAMA_BASE_URL = "http://localhost:11434"
    
    # Pastas
    PROJECTS_DIR = Path("projects")
    LOGS_DIR = Path("logs")
    
    # Parâmetros
    MAX_RETRIES = 3
    TEMPERATURE = 0.2
    TIMEOUT = 120
    
    # Validação
    ENABLE_SYNTAX_CHECK = True
    ENABLE_LLM_REVIEW = True
    
    @classmethod
    def init_dirs(cls):
        cls.PROJECTS_DIR.mkdir(exist_ok=True)
        cls.LOGS_DIR.mkdir(exist_ok=True)