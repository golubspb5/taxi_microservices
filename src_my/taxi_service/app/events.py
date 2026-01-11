# app/events.py
from fastapi import FastAPI
from threading import Thread
import time
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.matching_service import find_nearest_driver, check_assignment_timeouts
from app.models.trip import Trip, TripStatus

def start_background_tasks():
    """
    Запуск фоновых задач для проверки таймаутов и назначения водителей.
    """
    def background_loop():
        db: Session
        while True:
            try:
                db = SessionLocal()
                check_assignment_timeouts(db)
                # можно добавить вызов find_nearest_driver для новых поездок
            except Exception as e:
                print(f"Background task error: {e}")
            finally:
                db.close()
            time.sleep(5)  # проверка каждые 5 секунд

    thread = Thread(target=background_loop, daemon=True)
    thread.start()
