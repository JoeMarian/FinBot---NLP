
from finance.calculators import calculate_emi

def test_emi_basic():
    emi, schedule = calculate_emi(100000, 12, 1)
    assert round(emi, 2) > 0
    assert len(schedule) == 12
