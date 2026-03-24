# 🧠 AI Software Builder

Sistema de geração incremental de software com IA local via Ollama.

## 📋 Visão Geral

Este projeto transforma descrições em linguagem natural em aplicações completas, usando uma abordagem incremental e orquestrada para maior precisão.

```
Descrição → Planejamento → Tarefas → Geração → Revisão → Projeto Pronto
```

## 🚀 Instalação

### Pré-requisitos
- Python 3.9+
- [Ollama](https://ollama.com/) instalado e rodando

### Passo a Passo

1. **Clone ou baixe o projeto**
```bash
cd projeto_ia
```

2. **Crie o ambiente virtual**
```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

3. **Instale dependências**
```bash
pip install -r requirements.txt
```

4. **Inicie o Ollama** (em outro terminal)
```bash
ollama serve
```

5. **Baixe os modelos**
```bash
ollama pull llama3.2
ollama pull phi3
```

## 📖 Uso

### Comando Básico
```bash
python main.py <nome_projeto> "<descrição>"
```

### Exemplos
```bash
# API REST
python main.py api_blog "Crie uma API REST de blog com FastAPI"

# Site simples
python main.py portfolio "Site de portfólio em HTML/CSS"

# Script utilitário
python main.py scraper "Script Python para scraping de notícias"
```

## 📁 Estrutura Gerada
```
projects/
└── <nome_projeto>/
    ├── .ai_state.json    # Estado do projeto (não apague)
    ├── main.py
    ├── models.py
    ├── requirements.txt
    └── ...
```

## 🔧 Configuração

Edite `config.py` para personalizar:

```python
# Modelos
ARCHITECT_MODEL = "llama3.2"  # Para planejamento
CODER_MODEL = "phi3"          # Para geração de código
REVIEWER_MODEL = "llama3.2"   # Para revisão

# Validação
ENABLE_SYNTAX_CHECK = True    # Valida sintaxe Python
ENABLE_LLM_REVIEW = True      # Revisão via IA
MAX_RETRIES = 3               # Tentativas por tarefa
```

## 🐛 Troubleshooting

| Problema | Solução |
|----------|---------|
| `ConnectionError` | Execute `ollama serve` |
| `404 Not Found` | Atualize Ollama: `ollama pull <modelo>` |
| `Optional not defined` | Verifique imports em `state_manager.py` |
| Código com `\"` ou `\n` | O `CodeCleaner` corrige automaticamente |
| Modelo não encontrado | `ollama pull <nome_modelo>` |

## 📊 Logs

- **Console**: Visual em tempo real com Rich
- **Arquivo**: `logs/ai_builder.log` (detalhado)

Para debug, consulte o log:
```bash
tail -f logs/ai_builder.log
```

## 🔄 Como Funciona

1. **Planejamento**: IA define arquitetura e arquivos
2. **Tarefas**: Plano dividido em tarefas menores
3. **Geração**: Cada tarefa gera um arquivo
4. **Limpeza**: Remove artefatos de JSON/LLM
5. **Validação**: Check de sintaxe Python
6. **Revisão**: IA revisa código gerado

## 🎯 Melhorias Futuras

- [ ] Interface web (React + WebSocket)
- [ ] Integração Git automática
- [ ] Suporte a múltiplas linguagens
- [ ] Testes automáticos gerados
- [ ] Hot-reload de código gerado

## 📄 Licença

MIT - Use livremente!

---

**Desenvolvido com 🧠 IA Local + Python**