import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import flet as ft
from app.db_actions import *
import threading
from app.posture_monitor import PostureMonitor
import time

def create_card(task, on_delete, page):
    # Icono de prioridad
    if task.priority >= 5:
        priority_icon = ft.Icon(ft.Icons.PRIORITY_HIGH, color=ft.Colors.RED)
    elif task.priority >= 3:
        priority_icon = ft.Icon(ft.Icons.LOW_PRIORITY, color=ft.Colors.ORANGE)
    else:
        priority_icon = ft.Icon(ft.Icons.LOW_PRIORITY, color=ft.Colors.GREEN)

    # Icono de estado
    if task.status == "pending":
        status_icon = ft.Icon(ft.Icons.PENDING, color=ft.Colors.GREY)
    elif task.status == "in_progress":
        status_icon = ft.Icon(ft.Icons.AUTORENEW, color=ft.Colors.BLUE)
    elif task.status == "completed":
        status_icon = ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN)
    else:
        status_icon = ft.Icon(ft.Icons.HELP, color=ft.Colors.GREY)

    # Icono de tipo de tarea
    if task.type_task == "work":
        type_icon = ft.Icon(ft.Icons.WORK, color=ft.Colors.BLUE_GREY)
    elif task.type_task == "personal":
        type_icon = ft.Icon(ft.Icons.PERSON, color=ft.Colors.PINK)
    elif task.type_task == "study":
        type_icon = ft.Icon(ft.Icons.SCHOOL, color=ft.Colors.DEEP_PURPLE)
    else:
        type_icon = ft.Icon(ft.Icons.HELP, color=ft.Colors.GREY)

    if task.is_expired:
        due_date = f"Due_date: {task.due_date} (Expired)"
        due_date_color = ft.Colors.RED
    else:
        due_date = f"Due_date: {task.due_date}"
        due_date_color = ft.Colors.GREEN

    return ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.TASK),
                        title=ft.Text(task.title),
                        subtitle=ft.Text(task.description[:50]) 
                        if task.description else None,
                        trailing=ft.Text(due_date, color=due_date_color)
                    ),
                    ft.Container(content=ft.ResponsiveRow([
                        ft.Row([
                            priority_icon,
                            ft.Text(f"Priority: {task.priority}"),
                            status_icon,
                            ft.Text(f"Status: {task.status}"),
                            type_icon,
                            ft.Text(f"Type: {task.type_task}"),
                        ],col={"xs": 12, "sm": 4, "md": 3},alignment=ft.MainAxisAlignment.START,expand=True),
                        ft.Row([
                            ft.TextButton("View",on_click=lambda e: page.go(f"/view_screen?id={task.id}")),
                            ft.TextButton("Edit", on_click=lambda e: page.go(f"/update_task?id={task.id}")),
                            ft.TextButton("Delete", on_click=lambda e: on_delete(task.id))
                        ], col={"xs": 12, "sm": 4, "md": 3},alignment=ft.MainAxisAlignment.END,expand=True),
                    ],alignment=ft.MainAxisAlignment.SPACE_BETWEEN, expand=True),padding=10),
                ]
            ),
            padding=10,
        ), shadow_color=ft.Colors.ON_SURFACE_VARIANT,
    )

def main_screen(page: ft.Page):
    page.route == "/"
    page.title = "Main Screen"
    page.adaptive = True
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.scroll = "always"
    page.appbar = ft.AppBar(
        title=ft.Text("Workaware"),
        center_title=True,
        bgcolor=ft.Colors.BLUE_GREY_900,
        actions=[
            ft.IconButton(
                icon=ft.Icons.HOME,
                tooltip="main",
                on_click=lambda e: page.go("/")
            ),
            ft.IconButton(
                icon=ft.Icons.INFO,
                tooltip="About",
                on_click=lambda _: print("About clicked")
            )
        ])

    # Estado de los filtros
    filter_priority = ft.Dropdown(
        col={"xs": 12, "sm": 6, "md": 3},
        options=[
            ft.dropdownm2.Option("ALL"),
            ft.dropdownm2.Option("High Priority"),
            ft.dropdownm2.Option("Medium Priority"),
            ft.dropdownm2.Option("Low Priority"),
        ],
        expand=True,
        value="ALL"
    )
    filter_status = ft.Dropdown(
        col={"xs": 12, "sm": 6, "md": 3},
        options=[
            ft.dropdownm2.Option("ALL"),
            ft.dropdownm2.Option("Completed"),
            ft.dropdownm2.Option("In Progress"),
            ft.dropdownm2.Option("Pending"),
        ],
        expand=True,
        value="ALL"
    )
    filter_type = ft.Dropdown(
        col={"xs": 12, "sm": 6, "md": 3},
        options=[
            ft.dropdownm2.Option("ALL"),
            ft.dropdownm2.Option("Work"),
            ft.dropdownm2.Option("Personal"),
            ft.dropdownm2.Option("Study"),
        ],
        expand=True,
        value="ALL"
    )
    filter_due = ft.Dropdown(
        col={"xs": 12, "sm": 6, "md": 3},
        options=[
            ft.dropdownm2.Option("ALL"),
            ft.dropdownm2.Option("Less than 3 days"),
            ft.dropdownm2.Option("Less than 5 days"),
            ft.dropdownm2.Option("More than 7 days"),
        ],
        expand=True,
        value="ALL"
    )

    # Contenedor para la lista de tareas
    task_column = ft.Column(alignment=ft.MainAxisAlignment.CENTER)

    #crear control del hilo para el monitor de postura
    posture_monitor = None
    posture_thread = None

    def on_switch_change(e):
        nonlocal posture_monitor, posture_thread
        if e.control.value:
            # Crear nueva instancia cada vez que se activa
            posture_monitor = PostureMonitor()
            posture_thread = threading.Thread(target=posture_monitor.run, daemon=True)
            posture_thread.start()
        else:
            if posture_monitor and posture_thread and posture_thread.is_alive():
                posture_monitor.stop()
                posture_thread.join()
                page.open(ft.SnackBar(ft.Text(f"Posture monitoring summary: good posture: {time.strftime('%H:%M:%S', time.gmtime(posture_monitor.good_time))}, bad posture: {time.strftime('%H:%M:%S', time.gmtime(posture_monitor.bad_time))}.",), duration=5000))

    def on_delete_task(task_id):
        delete_task(get_db(), task_id)
        filter_tasks()

    def filter_tasks(*_):
        all_tasks = get_task_list(get_db())
        filtered = []
        for task in all_tasks:
            """Recorre todas las tareas y aplica los filtros seleccionados, si no se cumple la condicion 
            se salta a la siguiente tarea."""
            # Filtro prioridad 
            if filter_priority.value == "High Priority" and task.priority < 5:
                continue
            if filter_priority.value == "Medium Priority" and (task.priority < 3 or task.priority > 4):
                continue
            if filter_priority.value == "Low Priority" and task.priority > 2:
                continue
            # Filtro estado
            if filter_status.value == "Completed" and task.status != "completed":
                continue
            if filter_status.value == "In Progress" and task.status != "in_progress":
                continue
            if filter_status.value == "Pending" and task.status != "pending":
                continue
            # Filtro tipo
            if filter_type.value == "Work" and task.type_task != "work":
                continue
            if filter_type.value == "Personal" and task.type_task != "personal":
                continue
            if filter_type.value == "Study" and task.type_task != "study":
                continue
            # Filtro vencimiento
            from datetime import datetime, timedelta
            if filter_due.value == "Less than 3 days":
                try:
                    due = task.due_date
                    if isinstance(due, str):
                        due = datetime.strptime(due, "%Y-%m-%d").date()
                    if (due - datetime.now().date()).days >= 3:
                        continue
                except:
                    continue
            if filter_due.value == "Less than 5 days":
                try:
                    due = task.due_date
                    if isinstance(due, str):
                        due = datetime.strptime(due, "%Y-%m-%d").date()
                    if (due - datetime.now().date()).days >= 5:
                        continue
                except:
                    continue
            if filter_due.value == "More than 7 days":
                try:
                    due = task.due_date
                    if isinstance(due, str):
                        due = datetime.strptime(due, "%Y-%m-%d").date()
                    if (due - datetime.now().date()).days <= 7:
                        continue
                except:
                    continue
            filtered.append(task)
        task_column.controls = [create_card(task, on_delete_task, page) for task in filtered] if filtered else [ft.Text("No hay tareas registradas.")]
        page.update()

    # Asignar eventos
    filter_priority.on_change = filter_tasks
    filter_status.on_change = filter_tasks
    filter_type.on_change = filter_tasks
    filter_due.on_change = filter_tasks

    # Inicializar lista
    filter_tasks()
    
    page.add(
        ft.ResponsiveRow([
            ft.Column(
                [
                    ft.Text("Welcome to Workaware!", style=ft.TextStyle(size=24, weight=ft.FontWeight.BOLD)),
                    ft.Text("It's time to organize your day.", style=ft.TextStyle(size=16))
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=10,
                expand=True,
                col={"xs": 12, "sm": 5, "md": 4}
            ),
            ft.Container(
                content=ft.Switch(label="Posture monitoring", value=False, on_change=on_switch_change),
                alignment=ft.alignment.top_right,
                expand=True,
                col={"xs": 12, "sm": 5, "md": 2}
            ),
        ],alignment=ft.MainAxisAlignment.SPACE_BETWEEN, expand=True),
        
        
        
        
        ft.Divider(),
        ft.ResponsiveRow([
            filter_priority,
            filter_status,
            filter_type,
            filter_due,
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, expand=True),
        
        
        task_column,
        
        
        ft.Row([ft.ElevatedButton(
            "Add Task",
            on_click=lambda _: page.go("/add_task"),
            icon=ft.Icons.ADD,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.BLUE,
                shape=ft.RoundedRectangleBorder(radius=10)
            ),
        ),], alignment=ft.MainAxisAlignment.END)
    )

if __name__ == "__main__":
    ft.app(target=main_screen)