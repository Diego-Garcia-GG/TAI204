from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# 1. Definición del URL de conexión
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://admin:123456@postgres:5432/DB_miapi"
)

# 2. Se crea  el motor de conexión
engine = create_engine(DATABASE_URL)

# 3. Se crea la gestión de sesiones
SessionLocal= sessionmaker(
    autocommit= False,
    autoflush= False,
    bind= engine
)

# 4. Base declarativa para el Modelo
Base = declarative_base()

# 5. Función que trabaja sesiones con las peticiones
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()