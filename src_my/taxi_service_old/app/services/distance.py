def manhattan_distance(x1: int, y1: int, x2: int, y2: int) -> int:
    """
    Манхэттенское расстояние по сетке.
    """
    return abs(x1 - x2) + abs(y1 - y2)


def estimate_eta(distance: int, t_cell: int) -> int:
    """
    ETA = количество клеток * время на клетку.
    """
    return distance * t_cell


def estimate_price(base: float, per_cell: float, distance: int) -> float:
    """
    Цена поездки: base + distance * per_cell.
    """
    return base + distance * per_cell
