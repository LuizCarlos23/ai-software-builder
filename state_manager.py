import json
import os
from pathlib import Path
from typing import Optional, Dict, Any

class StateManager:
    def __init__(self, project_name: str):
        self.project_name = project_name
        # Garante que a pasta projects exista antes de criar o arquivo de estado
        self.state_file = Path(f"projects/{project_name}/.ai_state.json")
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.data = self.load()

    def load(self) -> dict:
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                # Se o arquivo estiver corrompido, reinicia o estado
                print("⚠️ Arquivo de estado corrompido. Reiniciando estado.")
                return {"status": "planning", "plan": [], "tasks": [], "completed_tasks": [], "files": []}
        return {"status": "planning", "plan": [], "tasks": [], "completed_tasks": [], "files": []}

    def save(self):
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def update_plan(self, plan: list):
        self.data["plan"] = plan
        self.data["status"] = "task_queue"
        self.save()

    def add_tasks(self, tasks: list):
        self.data["tasks"].extend(tasks)
        self.save()

    def get_next_task(self) -> Optional[Dict[str, Any]]:
        """Retorna a próxima tarefa ou None se a fila estiver vazia."""
        if self.data["tasks"]:
            return self.data["tasks"].pop(0)
        return None

    def mark_task_done(self, task: dict, file_path: str):
        self.data["completed_tasks"].append({**task, "file": file_path})
        self.data["files"].append(file_path)
        self.save()