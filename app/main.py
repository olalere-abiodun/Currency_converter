from fastapi import FastAPI
from .database import create_db_and_tables
from .dependencies import get_db
from . import schemas


app= FastAPI()


@app.get('/')
async def home():
    return {"message": "Welcome to Currency exchanger"}

