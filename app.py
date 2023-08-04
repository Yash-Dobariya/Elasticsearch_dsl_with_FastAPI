from src.crud.route import user
from fastapi import FastAPI
import uvicorn
from src.database import elasticsearch_connection

app = FastAPI()

app.include_router(user)
elasticsearch_connection()
