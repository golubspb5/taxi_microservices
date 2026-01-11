from fastapi import FastAPI
from app.core.db import engine, Base
from app.api.v1 import users, drivers, rides
from fastapi.middleware.cors import CORSMiddleware

# Создаём все таблицы при старте (для простого варианта)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Taxi Service", version="1.0")

# CORS (для фронтенда)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # на проде ставить конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Роутеры
app.include_router(users.router, prefix="/api/v1")
app.include_router(drivers.router, prefix="/api/v1")
app.include_router(rides.router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "Taxi Service API is running."}
