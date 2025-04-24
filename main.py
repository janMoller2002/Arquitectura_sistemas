from controllers.task_controller import TaskController
from views.task_view import display_menu, display_tasks

def main():
    controller = TaskController()

    while True:
        display_menu()
        option = input("Selecciona una opción: ")

        if option == "1":
            tasks = controller.list_tasks()
            display_tasks(tasks)
        elif option == "2":
            title = input("Título: ")
            description = input("Descripción (opcional): ")
            controller.add_task(title, description)
        elif option == "3":
            try:
                task_id = int(input("ID de la tarea a completar: "))
                if not controller.complete_task(task_id):
                    print("Tarea no encontrada.")
            except ValueError:
                print("ID inválido.")
        elif option == "4":
            try:
                task_id = int(input("ID de la tarea a eliminar: "))
                controller.delete_task(task_id)
            except ValueError:
                print("ID inválido.")
        elif option == "5":
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida. Intenta de nuevo.")

if __name__ == "__main__":
    main()
