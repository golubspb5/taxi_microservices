import pytest
from app.services.eta_service import calculate_eta

def test_eta_calculation():
    eta = calculate_eta(0, 0, 3, 4, t_cell=2)
    # расстояние = |3-0| + |4-0| = 7
    assert eta == 14
