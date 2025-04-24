def display_menu():
    print("\n--- GESTOR DE TAREAS ---")
    print("1. Listar tareas")
    print("2. Agregar tarea")
    print("3. Marcar tarea como completada")
    print("4. Eliminar tarea")
    print("5. Salir")

def display_tasks(tasks):
    if not tasks:
        print("No hay tareas.")
    for task in tasks:
        status = "✓" if task.completed else "✗"
        print(f"[{status}] {task.id}: {task.title} - {task.description}")
