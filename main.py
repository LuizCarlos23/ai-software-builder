import sys
from orchestrator import Orchestrator
from logger import log  # Importa para inicializar o logging

def main():
    # Inicializa o logging assim que o script roda
    log.info("=== Sistema Iniciado ===")

    if len(sys.argv) < 3:
        print("Uso: python main.py <nome_do_projeto> '<descrição>'")
        log.warning("Tentativa de execução sem argumentos corretos.")
        return

    project_name = sys.argv[1]
    user_request = " ".join(sys.argv[2:])

    log.info(f"Projeto: {project_name} | Request: {user_request}")

    try:
        app = Orchestrator(project_name, user_request)
        app.run()
    except KeyboardInterrupt:
        log.warning("Execução interrompida pelo usuário.")
        print("\n⚠️  Execução interrompida. O estado foi salvo.")
    except Exception as e:
        log.exception("Erro não tratado na aplicação principal.")
        print(f"❌ Erro fatal: {e}")

if __name__ == "__main__":
    main()