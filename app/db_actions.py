# Workaware - Copyright (c) 2025 Juan David Rivaldo Diaz Sierra
# www.linkedin.com/in/juan-david-rivaldo-diaz-sierra-72aa99222 
# Desarrollado por Juan David. Todos los derechos reservados.

from sqlalchemy.orm import Session
from database import SessionLocal
from models.task import Task

def get_db():
    db = SessionLocal()
    return db
        
def add_task(db:get_db, task: Task):
    db.query(Task).filter(Task.title == task.title).first()
    if db.query(Task).filter(Task.title == task.title).first():
        raise ValueError("Task with this title already exists.")
    if not task.title:
        raise ValueError("Task title cannot be empty.")
    if not task.due_date or not task.stimated_duration:
        raise ValueError("Due date and estimated duration are required.")
    if task.priority < 1 or task.priority > 5:
        raise ValueError("Priority must be between 1 and 5.")
    if task.status not in ['pending', 'in_progress', 'completed']:
        raise ValueError("Status must be one of: 'pending', 'in_progress', 'completed'.")
    if task.type_task not in ['work', 'personal', 'study']:
        raise ValueError("Type task must be one of: 'work', 'personal', 'study'.")
        
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_task(db: Session, task_id: int):
    if not task_id:
        raise ValueError("Task id cannot be empty.")
    return db.query(Task).filter(Task.id == task_id).first()

def get_task_list(db: Session):
    return db.query(Task).all()

def update_task(db: Session, task_id: int, **kwargs):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise ValueError("Task not found.")
    
    for key, value in kwargs.items():
        if hasattr(task, key):
            setattr(task, key, value)
        else:
            raise ValueError(f"Invalid field: {key}")
    
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise ValueError("Task not found.")
    
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully."}