from app.models.tariff import Tariff
from app.services.distance import manhattan_distance

def calculate_price(start: tuple[int, int], end: tuple[int, int], tariff: Tariff) -> float:
    """
    Рассчитывает стоимость поездки на основе Манхэттенского расстояния и тарифов.
    """
    distance = manhattan_distance(start, end)
    price = tariff.base_price + distance * tariff.price_per_cell
    return round(price, 2)
