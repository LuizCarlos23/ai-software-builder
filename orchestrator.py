import logging
from config import Config
from llm_client import OllamaClient
from state_manager import StateManager
from file_manager import FileManager
from code_cleaner import CodeCleaner
from code_validator import CodeValidator
from prompts import ARCHITECT_PROMPT, CODER_PROMPT, REVIEWER_PROMPT
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()
logger = logging.getLogger("AI_BUILDER")

class Orchestrator:
    def __init__(self, project_name: str, user_request: str):
        self.project_name = project_name
        self.user_request = user_request
        Config.init_dirs()
        self.state = StateManager(project_name)
        self.files = FileManager(f"projects/{project_name}")
        
        self.architect_llm = OllamaClient(model_name=Config.ARCHITECT_MODEL) 
        self.coder_llm = OllamaClient(model_name=Config.CODER_MODEL)
        self.reviewer_llm = OllamaClient(model_name=Config.REVIEWER_MODEL)
        
        logger.info(f"Orquestrador iniciado: {project_name}")

    def run(self):
        console.print(Panel(f"🚀 Projeto: {self.project_name}", style="bold green"))
        logger.info("=== INICIANDO FLUXO ===")
        
        try:
            if self.state.data["status"] == "planning":
                if not self._generate_architecture():
                    return
            
            if not self.state.data["tasks"] and self.state.data["status"] == "task_queue":
                self._generate_tasks()

            total_tasks = len(self.state.data["tasks"])
            if total_tasks == 0:
                console.print("[yellow]Nenhuma tarefa pendente.[/yellow]")
                return

            with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
                task_progress = progress.add_task("Gerando...", total=total_tasks)

                while True:
                    task = self.state.get_next_task()
                    if not task:
                        break
                    
                    progress.update(task_progress, description=f"Tarefa: {task['description']}")
                    success = self._execute_task_with_retry(task)
                    
                    if success:
                        progress.advance(task_progress)
                        console.print("[green]✓[/green]")
                    else:
                        console.print("[red]✗ Falha na tarefa[/red]")
                        logger.warning(f"Tarefa falhou: {task['description']}")

            # Fase de Revisão Final
            if Config.ENABLE_LLM_REVIEW:
                self._review_project()

            console.print(Panel("🎉 Projeto Concluído!", style="bold green"))
            logger.info("=== FLUXO CONCLUÍDO ===")

        except KeyboardInterrupt:
            logger.warning("Interrompido pelo usuário")
            console.print("\n[yellow]⚠️ Interrompido. Estado salvo.[/yellow]")
        except Exception as e:
            logger.exception(f"Erro crítico: {e}")
            console.print(f"[bold red]Erro: {e}[/bold red]")

    def _generate_architecture(self) -> bool:
        console.print("🧠 [bold blue]Fase 1: Arquitetura[/bold blue]")
        prompt = ARCHITECT_PROMPT.format(user_request=self.user_request)
        response = self.architect_llm.generate_json(prompt)
        
        if response and "files" in response:
            self.state.update_plan(response["files"])
            console.print(f"[green]✅ {len(response['files'])} arquivos planejados[/green]")
            return True
        console.print("[red]❌ Falha na arquitetura[/red]")
        return False

    def _generate_tasks(self):
        console.print("📋 [bold blue]Fase 2: Tarefas[/bold blue]")
        tasks = []
        for i, file_info in enumerate(self.state.data["plan"]):
            tasks.append({
                "id": i,
                "description": f"Criar {file_info['path']}",
                "files": [file_info["path"]]
            })
        self.state.add_tasks(tasks)
        logger.info(f"{len(tasks)} tarefas criadas")

    def _execute_task_with_retry(self, task) -> bool:
        """Executa tarefa com retries e validação."""
        file_path = task["files"][0]
        
        for attempt in range(Config.MAX_RETRIES):
            logger.info(f"Tentativa {attempt + 1}/{Config.MAX_RETRIES} para {file_path}")
            
            # Gera código
            code = self._generate_code(task)
            if not code:
                continue
            
            # Limpa código
            code = CodeCleaner.clean_code(code)
            
            # Valida sintaxe
            if Config.ENABLE_SYNTAX_CHECK and file_path.endswith('.py'):
                is_valid, error = CodeValidator.validate_python_syntax(code, file_path)
                if not is_valid:
                    logger.warning(f"Sintaxe inválida, retry...")
                    if attempt == Config.MAX_RETRIES - 1:
                        # Salva mesmo com erro na última tentativa
                        pass
                    else:
                        continue
            
            # Salva arquivo
            self.files.write_file(file_path, code)
            self.state.mark_task_done(task, file_path)
            return True
        
        return False

    def _generate_code(self, task) -> str:
        """Gera código via LLM."""
        file_path = task["files"][0]
        context = str(self.state.data["plan"])
        
        # Detecta linguagem pelo extensão
        language = "Python" if file_path.endswith('.py') else "JavaScript" if file_path.endswith('.js') else "Code"
        
        prompt = CODER_PROMPT.format(
            file_path=file_path,
            project_context=context,
            task_description=task["description"],
            language=language
        )
        
        response = self.coder_llm.generate_json(prompt)
        return response.get("code") if response else None

    def _review_project(self):
        """Revisão final do projeto gerado."""
        console.print("🔍 [bold blue]Fase 3: Revisão[/bold blue]")
        logger.info("Iniciando revisão do projeto")
        
        issues_found = []
        
        for file_record in self.state.data.get("completed_tasks", []):
            file_path = file_record.get("file", "")
            if not file_path.endswith('.py'):
                continue
                
            full_path = self.files.base_path / file_path
            if not full_path.exists():
                continue
            
            with open(full_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            prompt = REVIEWER_PROMPT.format(file_path=file_path, code=code[:3000])  # Limita contexto
            response = self.reviewer_llm.generate_json(prompt)
            
            if response:
                if not response.get("approved", True):
                    issues = response.get("issues", [])
                    if issues:
                        issues_found.append({"file": file_path, "issues": issues})
                        console.print(f"[yellow]⚠️ {file_path}: {len(issues)} problema(s)[/yellow]")
        
        if issues_found:
            console.print(f"[yellow]⚠️ {len(issues_found)} arquivo(s) com problemas[/yellow]")
            logger.warning(f"Revisão encontrou {len(issues_found)} arquivos com issues")
        else:
            console.print("[green]✅ Todos os arquivos aprovados na revisão[/green]")
        
        return issues_found