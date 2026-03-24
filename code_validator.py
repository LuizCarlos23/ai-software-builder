import ast
import logging
from pathlib import Path
from typing import Tuple, Optional

logger = logging.getLogger("AI_BUILDER")

class CodeValidator:
    """Valida código gerado antes de salvar."""
    
    @staticmethod
    def validate_python_syntax(code: str, file_path: str) -> Tuple[bool, Optional[str]]:
        """
        Valida sintaxe Python.
        Retorna: (é_válido, mensagem_de_erro)
        """
        if not file_path.endswith('.py'):
            return True, None  # Só valida Python
        
        try:
            ast.parse(code)
            logger.info(f"✅ Sintaxe válida: {file_path}")
            return True, None
        except SyntaxError as e:
            error_msg = f"Erro de sintaxe em {file_path}: {e.msg} (linha {e.lineno})"
            logger.error(f"❌ {error_msg}")
            return False, error_msg
    
    @staticmethod
    def validate_file_exists(file_path: Path) -> bool:
        """Verifica se o arquivo foi criado."""
        return file_path.exists() and file_path.stat().st_size > 0