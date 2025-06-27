# Workaware - Copyright (c) 2025 Juan David Rivaldo Diaz Sierra
# www.linkedin.com/in/juan-david-rivaldo-diaz-sierra-72aa99222 
# Desarrollado por Juan David. Todos los derechos reservados.

from app.db_actions import *
import urllib.parse
import flet as ft
import asyncio
from Interface.main_screen import main_screen
from Interface.add_update_screen import add_screen, update_screen
from Interface.expand_task_screen import expand_task
from app.db_actions import get_task, get_db



def splash_screen(page: ft.Page):
    page.clean()
    #page.bgcolor = ft.Colors.BLUE_GREY_900
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.add(
        ft.Column([
            ft.Image(src="assets/icon.png", width=100, height=100),
            ft.Text("Workaware", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            ft.ProgressRing(color=ft.Colors.WHITE, width=40, height=40)
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )
    page.update()


async def flet_main(page: ft.Page):
    # Inicializa los atributos globales si no existen
    splash_screen(page)
    await asyncio.sleep(2)  # Espera 2 segundos
    page.go("/")

    def route_change(e):
        page.clean()
        # Detecta si el hilo está corriendo
        if page.route == "/" or page.route == "":
            main_screen(page)
        elif page.route == "/add_task":
            add_screen(page)
        elif page.route.startswith("/view_screen"):
            params = urllib.parse.parse_qs(page.route.split("?")[1]) if "?" in page.route else {}
            task_id_str = str(params.get("id", [None])[0])
            # Solo permitir números positivos
            if not (task_id_str and task_id_str.isdigit() and int(task_id_str) > 0):
                page.add(ft.Text(f"ID de tarea inválido o no proporcionado: {task_id_str}"))
                page.update()
                return
            task_id = int(task_id_str)
            db = get_db()
            task = get_task(db, task_id)
            db.close()
            if task:
                task_data = {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "status": task.status,
                    "priority": task.priority,
                    "due_date": str(task.due_date),
                    "stimated_duration": task.stimated_duration,
                    "type_task": task.type_task
                }
                expand_task(page, task_data)
            else:
                page.add(ft.Text("Tarea no encontrada"))

        elif page.route.startswith("/update_task"):
            params = urllib.parse.parse_qs(page.route.split("?")[1]) if "?" in page.route else {}
            task_id_str = str(params.get("id", [None])[0])
            # Solo permitir números positivos
            if not (task_id_str and task_id_str.isdigit() and int(task_id_str) > 0):
                page.add(ft.Text(f"ID de tarea inválido o no proporcionado: {task_id_str}"))
                page.update()
                return
            task_id = int(task_id_str)
            db = get_db()
            task = get_task(db, task_id)
            db.close()
            if task:
                task_data = {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "status": task.status,
                    "priority": task.priority,
                    "due_date": str(task.due_date),
                    "stimated_duration": task.stimated_duration,
                    "type_task": task.type_task
                }
                update_screen(page, task_data)
            else:
                page.add(ft.Text("Tarea no encontrada"))
        page.update()

    page.on_route_change = route_change
    page.go(page.route)


if __name__ == "__main__":
    ft.app(
        target=flet_main,
        assets_dir="assets/",
        name="WorkAware",
        #window_icon="assets/icon.ico"
    )



