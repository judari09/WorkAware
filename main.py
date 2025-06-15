# main.py
from core.posture_monitor import PostureMonitor
import threading
from structures.task import Task
from core.db_actions import *
import time
from database import engine
from structures.task import Base  # Asegúrate de que Task hereda de Base
from datetime import datetime

class Tasker():
    
    title: str
    description: str
    status: str  # e.g., 'pending', 'in_progress', 'completed'
    priority: int   # 1 is low priority, 5 is high priority
    due_date: str  # Store as ISO format string
    stimated_duration: int  # Duration in hours
    type_task: str  # e.g., 'work', 'personal', 'study'

def run_posture_monitor():
    monitor = PostureMonitor()
    monitor.run()

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    t1 = threading.Thread(target=run_posture_monitor, daemon=True)
    t1.start()
    time.sleep(5)  # Give the monitor some time to start
    print("Posture monitor started in a separate thread.")
    # Example usage of Tasker and database actions
    tasker = Tasker()
    print("ES HORA DE ORGANIZARTE")
    print("Bienvenido al gestor de tareas. Por favor, selecciona una opción:")
    while True:
        print("-"*50)
        print("1. Añadir tarea")
        print("2. Ver tareas")
        print("3. Actualizar tarea")
        print("4. Eliminar tarea")
        print("5. Salir")
        print("-"*50)
        choice = input("Selecciona una opción: ")
        if choice == '1':
            title = input("Título de la tarea: ")
            description = input("Descripción de la tarea: ")
            status = input("Estado (pending, in_progress, completed): ")
            priority = int(input("Prioridad (1-5): "))
            due_date = input("Fecha de vencimiento (YYYY-MM-DD): ")
            stimated_duration = int(input("Duración estimada en horas: "))
            type_task = input("Tipo de tarea (work, personal, study): ")

            #due_date = datetime.strptime(due_date, "%Y-%m-%d").date() if due_date else #None
            #now = datetime.now()
            #if due_date and due_date < now.date():
            #    print("La fecha de vencimiento no puede ser anterior a la fecha actual.")
            #    continue
            
            
            task = Task(
                title=title,
                description=description,
                status=status,
                priority=priority,
                due_date=due_date,
                stimated_duration=stimated_duration,
                type_task=type_task
            )
            add_task(get_db(), task)
            print("Tarea añadida exitosamente.")
        
        elif choice == '2':
            tasks = get_task_list(get_db())
            for task in tasks:
                if task.is_expired:
                    print(f"{task.id}: {task.title} - {task.status} (Expirada)")
                print(f"{task.id}: {task.title} - {task.status}")
        
        elif choice == '3':
            task_id = int(input("ID de la tarea a actualizar: "))
            field = input("Campo a actualizar (title, description, status, priority, due_date, stimated_duration, type_task): ")
            value = input(f"Nuevo valor para {field}: ")
            update_task(get_db(), task_id, **{field: value})
            print("Tarea actualizada exitosamente.")
        
        elif choice == '4':
            task_id = int(input("ID de la tarea a eliminar: "))
            delete_task(get_db(), task_id)
            print("Tarea eliminada exitosamente.")
        
        elif choice == '5':
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Inténtalo de nuevo.")



