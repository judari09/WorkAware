import flet as ft

def expand_task(page: ft.Page, task_data: dict):
    """
    Expands the task details in the Flet page.
    
    :param page: The Flet page where the task details will be displayed.
    :param task_data: A dictionary containing task details.
    """
    page.clean()

    # Iconos según los datos
    # Prioridad
    priority = task_data.get('priority', 1)
    if priority >= 5:
        priority_icon = ft.Icon(ft.Icons.PRIORITY_HIGH, color=ft.Colors.RED)
    elif priority >= 3:
        priority_icon = ft.Icon(ft.Icons.LOW_PRIORITY, color=ft.Colors.ORANGE)
    else:
        priority_icon = ft.Icon(ft.Icons.LOW_PRIORITY, color=ft.Colors.GREEN)

    # Estado
    status = task_data.get('status', 'pending')
    if status == "pending":
        status_icon = ft.Icon(ft.Icons.PENDING, color=ft.Colors.GREY)
    elif status == "in_progress":
        status_icon = ft.Icon(ft.Icons.AUTORENEW, color=ft.Colors.BLUE)
    elif status == "completed":
        status_icon = ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN)
    else:
        status_icon = ft.Icon(ft.Icons.HELP, color=ft.Colors.GREY)

    # Tipo de tarea
    type_task = task_data.get('type_task', 'work')
    if type_task == "work":
        type_icon = ft.Icon(ft.Icons.WORK, color=ft.Colors.BLUE_GREY)
    elif type_task == "personal":
        type_icon = ft.Icon(ft.Icons.PERSON, color=ft.Colors.PINK)
    elif type_task == "study":
        type_icon = ft.Icon(ft.Icons.SCHOOL, color=ft.Colors.DEEP_PURPLE)
    else:
        type_icon = ft.Icon(ft.Icons.HELP, color=ft.Colors.GREY)

    # Card con iconos y datos
    card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.TASK, color=ft.Colors.BLUE),
                    ft.Text(f"{task_data.get('title', 'N/A')}", size=22, weight="bold"),
                ], spacing=10),
                ft.Divider(),
                ft.Row([
                    ft.Icon(ft.Icons.DESCRIPTION, color=ft.Colors.GREY),
                    ft.Text(task_data.get('description', 'N/A'), size=16),
                ], spacing=10),
                ft.Row([
                    status_icon,
                    ft.Text(f"Estado: {status}", size=16),
                ], spacing=10),
                ft.Row([
                    priority_icon,
                    ft.Text(f"Prioridad: {priority}", size=16),
                ], spacing=10),
                ft.Row([
                    ft.Icon(ft.Icons.CALENDAR_MONTH, color=ft.Colors.BLUE),
                    ft.Text(f"Vencimiento: {task_data.get('due_date', 'N/A')}", size=16),
                ], spacing=10),
                ft.Row([
                    ft.Icon(ft.Icons.ACCESS_TIME, color=ft.Colors.ORANGE),
                    ft.Text(f"Duración estimada: {task_data.get('stimated_duration', 'N/A')} horas", size=16),
                ], spacing=10),
                ft.Row([
                    type_icon,
                    ft.Text(f"Tipo: {type_task}", size=16),
                ], spacing=10),
            ], spacing=15, expand=True),
            padding=20,
        ),
        shadow_color=ft.Colors.ON_SURFACE_VARIANT,
    )

    page.add(card)
    page.update()
