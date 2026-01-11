from app.services.distance import manhattan_distance
from app.models.tariff import Tariff

def calculate_eta(start: tuple[int, int], end: tuple[int, int], tariff: Tariff) -> int:
    """
    Рассчитывает ETA (в секундах) по Манхэттенскому расстоянию и времени на одну клетку.
    """
    distance = manhattan_distance(start, end)
    eta = distance * tariff.t_cell
    return eta
