from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os

# По умолчанию используем SQLite (для Amvera и локальных тестов)
# Если переменная DATABASE_URL задана, используем её (например, для PostgreSQL)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./visitors.db")

# Дополнительные настройки для SQLite и PostgreSQL
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
else:
    # Для PostgreSQL добавляем timezone UTC
    connect_args = {"options": "-c timezone=UTC"}

engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    connect_args=connect_args
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()