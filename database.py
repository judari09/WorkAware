# Workaware - Copyright (c) 2025 Juan David Rivaldo Diaz Sierra
# www.linkedin.com/in/juan-david-rivaldo-diaz-sierra-72aa99222 
# Desarrollado por Juan David. Todos los derechos reservados.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///devices.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()