from typing import Tuple

def manhattan_distance(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    """
    Рассчитывает Манхэттенское расстояние между двумя точками (x, y) на сетке.
    """
    x1, y1 = a
    x2, y2 = b
    return abs(x1 - x2) + abs(y1 - y2)
