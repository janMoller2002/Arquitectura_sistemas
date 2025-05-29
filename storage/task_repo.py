import json
import os
from models.task import Task

DATA_FILE = os.path.join(os.path.dirname(__file__), 'task.json')

def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as file:
        data = json.load(file)
        return [Task.from_dict(task) for task in data]

def save_tasks(tasks):
    with open(DATA_FILE, 'w') as file:
        json.dump([task.to_dict() for task in tasks], file, indent=2)
