
from nlp.slots import extract_slots

def test_slots_amounts():
    s = extract_slots("EMI for 10 lakh at 9% for 5 years")
    assert s["amount"] and s["interest_rate"] and s["tenure_years"]
