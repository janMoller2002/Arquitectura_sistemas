from flask import Flask, jsonify, request, redirect, url_for
import os
import json
import datetime

app = Flask(__name__)

TASKS_FILE = "tasks.json"
BALANCER_LOG = "balancer.log"

def log_balancer_event(event):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(BALANCER_LOG, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {event}\n")

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)

@app.route("/")
def index():
    tasks = load_tasks()
    html = "<h2>Lista de tareas</h2><ul>"
    for i, t in enumerate(tasks):
        estado = "✅" if t.get("completed") else "❌"
        html += f"<li>{estado} {t.get('title', '')} <form style='display:inline' method='post' action='/complete/{i}'><button>Completar</button></form> <form style='display:inline' method='post' action='/delete/{i}'><button>Eliminar</button></form></li>"
    html += "</ul><form method='post' action='/add'><input name='title' placeholder='Nueva tarea'><button>Añadir</button></form>"
    return html

@app.route("/api/tasks", methods=["GET"])
def api_get_tasks():
    return jsonify(load_tasks())

@app.route("/api/tasks", methods=["POST"])
def api_add_task():
    data = request.get_json(force=True)
    if not data or not data.get("title"):
        return jsonify({"error": "El título es requerido"}), 400
    tasks = load_tasks()
    new_task = {"title": data["title"], "completed": False}
    tasks.append(new_task)
    save_tasks(tasks)
    log_balancer_event(f"API: Nueva tarea añadida: {data['title']}")
    return jsonify(new_task), 201

@app.route("/api/tasks/<int:task_id>/complete", methods=["PUT"])
def api_complete_task(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks[task_id]["completed"] = True
        save_tasks(tasks)
        log_balancer_event(f"API: Tarea completada: {tasks[task_id]['title']}")
        return jsonify(tasks[task_id])
    return jsonify({"error": "Tarea no encontrada"}), 404

@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def api_delete_task(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        deleted = tasks.pop(task_id)
        save_tasks(tasks)
        log_balancer_event(f"API: Tarea eliminada: {deleted['title']}")
        return jsonify(deleted)
    return jsonify({"error": "Tarea no encontrada"}), 404

@app.route("/add", methods=["POST"])
def web_add_task():
    title = request.form.get("title")
    if title:
        tasks = load_tasks()
        tasks.append({"title": title, "completed": False})
        save_tasks(tasks)
        log_balancer_event(f"WEB: Nueva tarea añadida: {title}")
    return redirect(url_for("index"))

@app.route("/complete/<int:task_id>", methods=["POST"])
def web_complete_task(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks[task_id]["completed"] = True
        save_tasks(tasks)
        log_balancer_event(f"WEB: Tarea completada: {tasks[task_id]['title']}")
    return redirect(url_for("index"))

@app.route("/delete/<int:task_id>", methods=["POST"])
def web_delete_task(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        deleted = tasks.pop(task_id)
        save_tasks(tasks)
        log_balancer_event(f"WEB: Tarea eliminada: {deleted['title']}")
    return redirect(url_for("index"))

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
