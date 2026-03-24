import requests
import json
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger("AI_BUILDER")

class OllamaClient:
    def __init__(self, model_name: str = "llama3.2"):
        self.base_url = "http://localhost:11434"
        self.generate_url = f"{self.base_url}/api/generate"
        self.model = model_name
        logger.info(f"Cliente Ollama inicializado. URL: {self.generate_url} | Modelo: {model_name}")

    def generate_json(self, prompt: str, system_prompt: str = "") -> Optional[Dict[str, Any]]:
        logger.debug(f"Enviando prompt para {self.model}...")
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "system": system_prompt,
            "format": "json",
            "stream": False,
            "options": {"temperature": 0.2}
        }

        try:
            # Primeiro, vamos testar se a API está viva
            try:
                health_check = requests.get(f"{self.base_url}/api/tags", timeout=5)
                if health_check.status_code != 200:
                    logger.warning(f"API Tags retornou status {health_check.status_code}. Pode haver problemas.")
            except Exception as e:
                logger.error(f"Não foi possível conectar ao Ollama em {self.base_url}. Ele está rodando? Erro: {e}")
                return None

            # Agora tenta gerar
            response = requests.post(self.generate_url, json=payload, timeout=120)
            
            # LOG DETALHADO DE ERRO HTTP
            if response.status_code != 200:
                logger.error(f"❌ Erro HTTP {response.status_code}: {response.text}")
                logger.error(f"URL tentada: {self.generate_url}")
                logger.error(f"Possível causa: Modelo '{self.model}' não existe ou URL incorreta.")
                return None

            data = response.json()
            raw_content = data.get("response", "")
            
            if not raw_content:
                logger.warning("A IA retornou uma resposta vazia.")
                return None

            logger.debug(f"Resposta Bruta (início): {raw_content[:150]}...")

            try:
                parsed_json = json.loads(raw_content)
                logger.info("JSON parseado com sucesso.")
                return parsed_json
            except json.JSONDecodeError as e:
                logger.error(f"❌ ALUCINAÇÃO DE FORMATO: A IA não retornou JSON válido. Erro: {e}")
                logger.error(f"Conteúdo recebido: {raw_content}")
                return None

        except requests.exceptions.ConnectionError:
            logger.error("❌ Erro de Conexão: Ollama não está respondendo em localhost:11434.")
            logger.error("Dica: Execute 'ollama serve' em outro terminal.")
            return None
        except requests.exceptions.Timeout:
            logger.error("❌ Timeout: A IA demorou muito para responder.")
            return None
        except Exception as e:
            logger.exception(f"❌ Erro inesperado: {e}")
            return None