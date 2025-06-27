# Workaware v1.0.0

**Workaware** es una aplicación de escritorio multiplataforma para la gestión de tareas y el monitoreo de postura, desarrollada en Python usando [Flet](https://flet.dev/).

---

## Funcionalidades principales

- **Gestión de tareas:**  
  Añade, edita, elimina y visualiza tareas con campos como prioridad, estado, tipo, fecha de vencimiento y duración estimada.

- **Filtros avanzados:**  
  Filtra tareas por prioridad, estado y tipo usando menús desplegables responsivos.

- **Monitoreo de postura:**  
  Activa o desactiva el monitor de postura con un switch. Recibe notificaciones y alertas sonoras si se detecta mala postura.

- **Notificaciones de escritorio:**  
  Recibe alertas visuales y sonoras cuando se detecta mala postura.

- **Interfaz moderna y responsive:**  
  Uso de iconos, tarjetas y diseño adaptable a cualquier tamaño de ventana.

- **Persistencia:**  
  Base de datos SQLite gestionada con SQLAlchemy.

---

## Captura de pantalla


![Captura de pantalla de Workaware](workaware_screen.png)

---

## Estructura del proyecto

```
workaware/
│
├── app/
│   ├── db_actions.py
│   ├── notifier.py
│   ├── posture_monitor.py
│   ├── session_logger.py
│   └── ...
│
├── detector/
│   └── detector.py
│
├── Interface/
│   ├── main_screen.py
│   ├── add_update_screen.py
│   ├── expand_task_screen.py
│   └── ...
│
├── models/
│   └── task.py
│
├── sounds/
│   └── ...
│
├── assets/
│   └── workaware.ico
│
├── database.py
├── devices.db
├── main.py
├── README.md
├── requirements.txt
└── ...
```

---

## Créditos

Desarrollado por Juan David y colaboradores.  
Basado en Flet, SQLAlchemy, Plyer, Pygame y otras librerías de código abierto.