from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

app = FastAPI()

# Database configuration
DB_USER = os.getenv('DB_USER', 'raam')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'raam')
DB_HOST = os.getenv('DB_HOST', '10.9.4.4')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_NAME = os.getenv('DB_NAME', 'data_management')
DB_CHARSET = os.getenv('DB_CHARSET', 'utf8mb4')
DB_COLLATION = os.getenv('DB_COLLATION', 'utf8mb4_general_ci')

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset={DB_CHARSET}"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

@app.get("/")
def read_root():
    return {"message": "Personal Details API is running"} 