from fastapi import FastAPI
from sqlalchemy.orm import Session
from app.api import auth, passenger, driver, trips
from app.events import start_background_tasks
from app.database import Base, engine

# создаем таблицы при старте (можно потом перейти на Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Taxi Service")

# роутеры
app.include_router(auth.router, prefix="/api/v1")
app.include_router(passenger.router, prefix="/api/v1")
app.include_router(driver.router, prefix="/api/v1")
app.include_router(trips.router, prefix="/api/v1")

# запускаем фоновые задачи на старте
@app.on_event("startup")
async def startup_event():
    start_background_tasks()
