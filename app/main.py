from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database import create_db_and_tables
from app.router import auth, currency, historical, favorites

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    create_db_and_tables()
    yield
    # Shutdown logic (if any)

# Create app with lifespan
app = FastAPI(lifespan=lifespan)

# Include routers
app.include_router(auth.router)
app.include_router(currency.router)
app.include_router(historical.router)
app.include_router(favorites.router)

@app.get("/")
async def home():
    return {"message": "Welcome to Currency exchanger"}
