from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./visitors.db")

connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
else:
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

# ===== ВАЖНО: создаём таблицы при импорте =====
Base.metadata.create_all(bind=engine)
print("Таблицы проверены/созданы")