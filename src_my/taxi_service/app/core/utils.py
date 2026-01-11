from datetime import datetime

def current_utc_time() -> datetime:
    return datetime.utcnow()

def calculate_eta(distance_cells: int, t_cell: int) -> int:
    """
    Рассчитывает ETA в секундах, исходя из расстояния по клеткам и времени t_cell на шаг.
    """
    return distance_cells * t_cell
