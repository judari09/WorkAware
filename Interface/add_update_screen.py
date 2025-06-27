# Workaware - Copyright (c) 2025 Juan David Rivaldo Diaz Sierra
# www.linkedin.com/in/juan-david-rivaldo-diaz-sierra-72aa99222 
# Desarrollado por Juan David. Todos los derechos reservados.

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import flet as ft
import datetime
from app.db_actions import *

def add_screen(page: ft.Page):
    appbar = ft.AppBar(
        leading=ft.Icon(ft.Icons.TASK),
        title=ft.Text("Añadir Tarea"),
        bgcolor=ft.Colors.BLUE,
        center_title=True,
        actions=[
            ft.IconButton(ft.Icons.CLOSE, on_click=lambda e: page.go("/"))
        ]
    )
    #listas de opciones para los dropdowns
    priority  = [
       ft.dropdown.Option("1 (Baja)", leading_icon=ft.Icon(ft.Icons.LOW_PRIORITY, color=ft.Colors.BLUE)),
       ft.dropdown.Option("2 (Media baja)", leading_icon=ft.Icon(ft.Icons.LOW_PRIORITY, color=ft.Colors.GREEN)),
       ft.dropdown.Option("3 (Media)", leading_icon=ft.Icon(ft.Icons.DRAG_HANDLE,color=ft.Colors.YELLOW)),
       ft.dropdown.Option("4 (Media alta)", leading_icon=ft.Icon(ft.Icons.PRIORITY_HIGH,color=ft.Colors.ORANGE)),
       ft.dropdown.Option("5 (Alta)", leading_icon=ft.Icon(ft.Icons.PRIORITY_HIGH, color=ft.Colors.RED))]
    
    type_task = [
        ft.dropdown.Option("Work (Trabajo)", leading_icon=ft.Icon(ft.Icons.WORK, color=ft.Colors.BLUE)),
        ft.dropdown.Option("Personal (Personal)",leading_icon=ft.Icon(ft.Icons.PERSON, color=ft.Colors.GREEN)),
        ft.dropdown.Option("Study (Estudio)", leading_icon=ft.Icon(ft.Icons.BOOK, color=ft.Colors.YELLOW))]
    
    status = [
        ft.dropdown.Option("Pending (Pendiente)", leading_icon=ft.Icon(ft.Icons.PENDING, color=ft.Colors.ORANGE)),
        ft.dropdown.Option("In_progress (En progreso)",leading_icon=ft.Icon(ft.Icons.AUTORENEW, color=ft.Colors.BLUE)),
        ft.dropdown.Option("Completed (Completada)", leading_icon=ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN))]
    
    #campo de texto para la fecha de vencimiento
    selected_due_date = ft.Text("No hay fecha seleccionada", size=14, color=ft.Colors.GREY)
    due_date_value = {"value": None}

    #logica para el selector de fecha 
    def date_picker_changed(e):
        if e.control.value:
            fecha = e.control.value.strftime("%Y-%m-%d")
            selected_due_date.value = fecha
            due_date_value["value"] = fecha
            page.update()
    ## objeto DatePicker para seleccionar la fecha de vencimiento
    ## y un boton para abrir el selector de fecha
    due_date_picker = ft.DatePicker(
        first_date=datetime.datetime.now(),
        last_date=datetime.datetime(year=2100, month=12, day=31),
        on_change=date_picker_changed
    )
    page.overlay.append(due_date_picker) #sobreponer el DatePicker en la pagina
    due_date_input = ft.ElevatedButton(
        "Seleccionar Fecha de Vencimiento", icon=ft.Icons.CALENDAR_TODAY,
        on_click=lambda e: page.open(due_date_picker),
    )

    #campos de entrada para el titulo de la tarea, limitado a 100 caracteres,
    title_input = ft.TextField(label="Título de la tarea", autofocus=True, max_length=100, multiline=True)
    
    #campo de entrada para la descripcion de la tarea, limitado a 500 caracteres
    description_input = ft.TextField(label="Descripción de la tarea", max_length=500, multiline=True,helper="Descripción opcional de la tarea")
    
    #dropdowns para el estado, prioridad y tipo de tarea
    status_input = ft.Dropdown(
        label="Estado de la tarea",
        editable=False,
        options=status,
        expand=True)
    
    priority_input = ft.Dropdown(
        label="Prioridad (1-5)",
        editable=False,
        options=priority,
        expand=True)
    
    # Contador para duración estimada en horas
    stimated_duration_value = {"value": 1}
    stimated_duration_text = ft.Text(str(stimated_duration_value["value"]), size=16)

    def increase_duration(e):
        stimated_duration_value["value"] += 1
        stimated_duration_text.value = str(stimated_duration_value["value"])
        page.update()

    def decrease_duration(e):
        if stimated_duration_value["value"] > 1:
            stimated_duration_value["value"] -= 1
            stimated_duration_text.value = str(stimated_duration_value["value"])
            page.update()

    stimated_duration_input = ft.Row([
        ft.Text("Duración estimada en horas", size=14),
        ft.IconButton(ft.Icons.REMOVE, on_click=decrease_duration),
        stimated_duration_text,
        ft.IconButton(ft.Icons.ADD, on_click=increase_duration),
    ], alignment=ft.MainAxisAlignment.START, spacing=5)

    type_task_input = ft.Dropdown(
        label="Tipo de tarea",
        editable=False,
        options=type_task,
        expand=True)

    def submit(e):
        db = get_db()
        try:
            # Extraer valores clave de los dropdowns
            priority_val = int(priority_input.value.split()[0]) if priority_input.value else 1
            type_task_val = type_task_input.value.split()[0].lower() if type_task_input.value else "work"
            status_val = status_input.value.split()[0].lower() if status_input.value else "pending"
            # Validar campos requeridos
            if not title_input.value or not due_date_value["value"] or not stimated_duration_value["value"]:
                page.open(ft.SnackBar(ft.Text("Por favor, completa todos los campos obligatorios.")))
                page.update()
                return
            task = Task(
                title=title_input.value,
                description=description_input.value,
                status=status_val,
                priority=priority_val,
                due_date=due_date_value["value"],
                stimated_duration=stimated_duration_value["value"],
                type_task=type_task_val
            )
            add_task(db, task)
            page.open(ft.SnackBar(ft.Text("Tarea añadida exitosamente.")))
            page.update()
            page.go("/")  # Redirigir a la pantalla principal después de añadir
        except Exception as ex:
            page.open(ft.SnackBar(ft.Text(f"Error: {str(ex)}")))
            page.update()
        finally:
            db.close()

    submit_button = ft.ElevatedButton("Añadir nueva Tarea", on_click=submit)

    form_column = ft.Column([
        ft.Text("Rellena los campos para añadir una nueva tarea", size=18, weight=ft.FontWeight.NORMAL),
        ft.Divider(),
        title_input,
        description_input,
        status_input,
        priority_input,
        ft.ResponsiveRow([
            due_date_input,
            selected_due_date
        ],col={"xs": 12, "sm": 6, "md": 6}, alignment=ft.MainAxisAlignment.START,expand=True),
        stimated_duration_input,
        type_task_input,
        submit_button
    ],
    alignment=ft.MainAxisAlignment.CENTER,
    spacing=15,
    scroll="auto",
    expand=True
    )

    page.add(
        appbar,
        ft.Container(
            content=form_column,
            alignment=ft.alignment.top_center,
            padding=20,
            expand=True
        )
    )
   

def update_screen(page: ft.Page, task_data=None):
    appbar = ft.AppBar(
        leading=ft.Icon(ft.Icons.TASK),
        title=ft.Text("Actualizar Tarea"),
        bgcolor=ft.Colors.BLUE,
        center_title=True,
        actions=[
            ft.IconButton(ft.Icons.CLOSE, on_click=lambda e: page.go("/"))
        ]
    )
    # Listas de opciones para los dropdowns
    priority  = [
       ft.dropdown.Option("1 (Baja)", leading_icon=ft.Icon(ft.Icons.LOW_PRIORITY, color=ft.Colors.BLUE)),
       ft.dropdown.Option("2 (Media baja)", leading_icon=ft.Icon(ft.Icons.LOW_PRIORITY, color=ft.Colors.GREEN)),
       ft.dropdown.Option("3 (Media)", leading_icon=ft.Icon(ft.Icons.DRAG_HANDLE,color=ft.Colors.YELLOW)),
       ft.dropdown.Option("4 (Media alta)", leading_icon=ft.Icon(ft.Icons.PRIORITY_HIGH,color=ft.Colors.ORANGE)),
       ft.dropdown.Option("5 (Alta)", leading_icon=ft.Icon(ft.Icons.PRIORITY_HIGH, color=ft.Colors.RED))]
    
    type_task = [
        ft.dropdown.Option("Work (Trabajo)", leading_icon=ft.Icon(ft.Icons.WORK, color=ft.Colors.BLUE)),
        ft.dropdown.Option("Personal (Personal)",leading_icon=ft.Icon(ft.Icons.PERSON, color=ft.Colors.GREEN)),
        ft.dropdown.Option("Study (Estudio)", leading_icon=ft.Icon(ft.Icons.BOOK, color=ft.Colors.YELLOW))]
    
    status = [
        ft.dropdown.Option("Pending (Pendiente)", leading_icon=ft.Icon(ft.Icons.PENDING, color=ft.Colors.ORANGE)),
        ft.dropdown.Option("In_progress (En progreso)",leading_icon=ft.Icon(ft.Icons.AUTORENEW, color=ft.Colors.BLUE)),
        ft.dropdown.Option("Completed (Completada)", leading_icon=ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN))]
    
    # Campo de texto para la fecha de vencimiento
    selected_due_date = ft.Text("No hay fecha seleccionada", size=14, color=ft.Colors.GREY)
    due_date_value = {"value": None}

    # Lógica para el selector de fecha 
    def date_picker_changed(e):
        if e.control.value:
            fecha = e.control.value.strftime("%Y-%m-%d")
            selected_due_date.value = fecha
            due_date_value["value"] = fecha
            page.update()
    
    due_date_picker = ft.DatePicker(
        first_date=datetime.datetime.now(),
        last_date=datetime.datetime(year=2100, month=12, day=31),
        on_change=date_picker_changed
    )
    page.overlay.append(due_date_picker)
    due_date_input = ft.ElevatedButton(
        "Seleccionar Fecha de Vencimiento", icon=ft.Icons.CALENDAR_TODAY,
        on_click=lambda e: page.open(due_date_picker),
    )

    # Prefill values if task_data is provided
    title_val = task_data["title"] if task_data else ""
    description_val = task_data["description"] if task_data else ""
    status_val = None
    priority_val = None
    type_task_val = None
    due_date_val = None
    stimated_duration_val = 1
    if task_data:
        # Map DB values to dropdown display values
        status_map = {
            "pending": "Pending (Pendiente)",
            "in_progress": "In progress (En progreso)",
            "completed": "Completed (Completada)"
        }
        type_map = {
            "work": "Work (Trabajo)",
            "personal": "Personal (Personal)",
            "study": "Study (Estudio)"
        }
        status_val = status_map.get(task_data["status"], None)
        priority_val = f"{task_data['priority']}"  # Will match start of dropdown value
        type_task_val = type_map.get(task_data["type_task"], None)
        due_date_val = task_data["due_date"]
        stimated_duration_val = task_data["stimated_duration"]
        selected_due_date.value = due_date_val
        due_date_value["value"] = due_date_val

    title_input = ft.TextField(label="Título de la tarea", autofocus=True, max_length=100, multiline=True, value=title_val)
    description_input = ft.TextField(label="Descripción de la tarea", max_length=500, multiline=True, helper="Descripción opcional de la tarea", value=description_val)
    status_input = ft.Dropdown(
        label="Estado de la tarea",
        editable=False,
        options=status,
        value=status_val,
        expand=True)
    priority_input = ft.Dropdown(
        label="Prioridad (1-5)",
        editable=False,
        options=priority,
        value=None,
        expand=True)
    # Set priority value by matching prefix
    if priority_val:
        for opt in priority:
            if opt.key.startswith(priority_val):
                priority_input.value = opt.key
                break
    type_task_input = ft.Dropdown(
        label="Tipo de tarea",
        editable=False,
        options=type_task,
        value=type_task_val,
        expand=True)

    stimated_duration_value = {"value": stimated_duration_val}
    stimated_duration_text = ft.Text(str(stimated_duration_value["value"]), size=16)

    def increase_duration(e):
        stimated_duration_value["value"] += 1
        stimated_duration_text.value = str(stimated_duration_value["value"])
        page.update()

    def decrease_duration(e):
        if stimated_duration_value["value"] > 1:
            stimated_duration_value["value"] -= 1
            stimated_duration_text.value = str(stimated_duration_value["value"])
            page.update()

    stimated_duration_input = ft.Row([
        ft.Text("Duración estimada en horas", size=14),
        ft.IconButton(ft.Icons.REMOVE, on_click=decrease_duration),
        stimated_duration_text,
        ft.IconButton(ft.Icons.ADD, on_click=increase_duration),
    ], alignment=ft.MainAxisAlignment.START, spacing=5)

    def submit(e):
        db = get_db()
        try:
            # Extraer valores clave de los dropdowns
            priority_val = int(priority_input.value.split()[0]) if priority_input.value else 1
            type_task_val = type_task_input.value.split()[0].lower() if type_task_input.value else "work"
            status_val = status_input.value.split()[0].lower() if status_input.value else "pending"
            # Validar campos requeridos
            if not title_input.value or not due_date_value["value"] or not stimated_duration_value["value"]:
                page.open(ft.SnackBar(ft.Text("Por favor, completa todos los campos obligatorios.")))
                page.update()
                return
            # Llamar a update_task con los campos modificados
            update_task(db, task_data["id"],
                title=title_input.value,
                description=description_input.value,
                status=status_val,
                priority=priority_val,
                due_date=due_date_value["value"],
                stimated_duration=stimated_duration_value["value"],
                type_task=type_task_val
            )
            page.open(ft.SnackBar(ft.Text("Tarea actualizada exitosamente.")))
            page.update()
            page.go("/")
        except Exception as ex:
            page.open(ft.SnackBar(ft.Text(f"Error: {str(ex)}")))
            page.update()
        finally:
            db.close()

    submit_button = ft.ElevatedButton("Actualizar Tarea", on_click=submit)

    form_column = ft.Column([
        ft.Text("Edita los campos para actualizar la tarea", size=18, weight=ft.FontWeight.NORMAL),
        ft.Divider(),
        title_input,
        description_input,
        status_input,
        priority_input,
        ft.ResponsiveRow([
            due_date_input,
            selected_due_date
        ],col={"xs": 12, "sm": 6, "md": 6}, alignment=ft.MainAxisAlignment.START,expand=True),
        stimated_duration_input,
        type_task_input,
        submit_button
    ],
    alignment=ft.MainAxisAlignment.CENTER,
    spacing=15,
    scroll="auto",
    expand=True
    )

    page.add(
        appbar,
        ft.Container(
            content=form_column,
            alignment=ft.alignment.top_center,
            padding=20,
            expand=True
        )
    ) 
    
#ft.app(target=update_screen)