from sqlalchemy import Column, Integer, String
from database import Base
from datetime import datetime

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    status = Column(String, index=True)  # e.g., 'pending', 'in_progress', 'completed'
    priority = Column(Integer, default=1)  # 1 is low priority, 5 is high priority
    due_date = Column(String, index=True)  # Store as ISO format string
    stimated_duration = Column(Integer, default=0)  # Duration in hours
    type_task = Column(String, index=True)  # e.g., 'work', 'personal', 'study'

    @property
    def is_expired(self):
        if not self.due_date:
            return False
        try:
            due = self.due_date
            if isinstance(due, str):
                due = datetime.strptime(due, "%Y-%m-%d").date()
            return due < datetime.now().date()
        except Exception:
            return False
