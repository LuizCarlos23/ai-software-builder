import re
import logging

logger = logging.getLogger("AI_BUILDER")

class CodeCleaner:
    """Limpa artefatos de JSON/LLM do código gerado."""
    
    @staticmethod
    def clean_code(raw_code: str) -> str:
        """Remove artefatos comuns de geração via JSON."""
        code = raw_code
        
        # 1. Remove markdown code blocks se existirem
        code = re.sub(r'```python\s*', '', code)
        code = re.sub(r'```json\s*', '', code)
        code = re.sub(r'```\s*', '', code)
        
        # 2. Converte escapes de JSON de volta para caracteres reais
        code = code.replace('\\n', '\n')
        code = code.replace('\\"', '"')
        code = code.replace("\\'", "'")
        code = code.replace('\\\\', '\\')
        code = code.replace('\\t', '\t')
        
        # 3. Remove espaços extras no início/fim
        code = code.strip()
        
        # 4. Remove textos tipo "Claro, aqui está o código:"
        patterns_to_remove = [
            r'^[A-Za-z\s,]+:$',
            r'^Aqui está o código.*$',
            r'^Claro.*$',
            r'^Segue o código.*$',
        ]
        for pattern in patterns_to_remove:
            code = re.sub(pattern, '', code, flags=re.MULTILINE | re.IGNORECASE)
        
        # 5. Garante que termina com newline
        if code and not code.endswith('\n'):
            code += '\n'
        
        logger.debug(f"Código limpo: {len(code)} caracteres")
        return code