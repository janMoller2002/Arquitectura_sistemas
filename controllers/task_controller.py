from storage.task_repo import load_tasks, save_tasks
from models.task import Task

class TaskController:
    def __init__(self):
        self.tasks = load_tasks()
        self.next_id = max([t.id for t in self.tasks], default=0) + 1

    def list_tasks(self):
        return self.tasks

    def add_task(self, title, description=""):
        task = Task(self.next_id, title, description)
        self.tasks.append(task)
        self.next_id += 1
        save_tasks(self.tasks)

    def complete_task(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                task.completed = True
                save_tasks(self.tasks)
                return True
        return False

    def delete_task(self, task_id):
        self.tasks = [task for task in self.tasks if task.id != task_id]
        save_tasks(self.tasks)
