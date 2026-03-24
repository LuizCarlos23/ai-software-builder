import logging
import sys
from pathlib import Path
from rich.logging import RichHandler
from rich.console import Console

# Cria pasta de logs se não existir
Path("logs").mkdir(exist_ok=True)

# Configuração do Logger
def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG) # Nível detalhado para arquivo

    # Limpa handlers anteriores para evitar duplicação
    if not logger.handlers:
        # 1. Handler para Arquivo (Detalhado)
        file_handler = logging.FileHandler("logs/ai_builder.log", encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_format)

        # 2. Handler para Console (Visual com Rich)
        console_handler = RichHandler(rich_tracebacks=True, show_time=False, show_path=False)
        console_handler.setLevel(logging.INFO) # Menos ruído no console
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

# Logger global para o sistema
log = get_logger("AI_BUILDER")