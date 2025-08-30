
import re

_CURRENCY = r"(?:₹|INR\s*)?"
_NUM = r"(?:(?:\d{1,3}(?:,\d{3})+)|\d+\.?\d*)"
_AMOUNT = rf"{_CURRENCY}{_NUM}\s*(?:lakh|lac|L|L\b|crore|Cr)?"
_DURATION = r"(\d+\.?\d*)\s*(years?|yrs?|y|months?|mos?|m)"
_RATE = r"(\d+\.?\d*)\s*%"
_PER_MONTH = r"(per\s*month|/month|monthly|per\s*mth|pm)"

def _to_amount(s: str):
    s = s.replace(",", "").strip()
    mul = 1.0
    if re.search(r"crore|Cr", s, re.I):
        mul = 1e7
        s = re.sub(r"(crore|Cr)", "", s, flags=re.I)
    elif re.search(r"lakh|lac|\bL\b", s, re.I):
        mul = 1e5
        s = re.sub(r"(lakh|lac|\bL\b)", "", s, flags=re.I)
    s = s.replace("₹", "").replace("INR", "")
    try:
        return float(s) * mul
    except:
        return None

def extract_slots(text: str):
    t = text.lower()

    # amounts
    amounts = []
    for m in re.finditer(rf"{_CURRENCY}({_NUM})(?:\s*(lakh|lac|l|crore|cr))?", t, re.I):
        num = m.group(1)
        unit = m.group(2)
        val = float(num.replace(",", ""))
        if unit:
            if re.search(r"crore|cr", unit, re.I): val *= 1e7
            elif re.search(r"lakh|lac|\bl\b", unit, re.I): val *= 1e5
        amounts.append(val)

    # interest rate
    rate = None
    m = re.search(_RATE, t, re.I)
    if m:
        rate = float(m.group(1))

    # duration
    years = months = None
    for m in re.finditer(_DURATION, t, re.I):
        val = float(m.group(1))
        unit = m.group(2)
        if unit.startswith("y"):
            years = val
        else:
            months = val

    # salary & expenses monthly markers
    salary_m = None
    expenses_m = None
    # salary per month
    for m in re.finditer(rf"{_CURRENCY}({_NUM})\s*(lakh|lac|l|crore|cr)?\s*{_PER_MONTH}", t, re.I):
        num = float(m.group(1).replace(",", ""))
        unit = m.group(2)
        mul = 1.0
        if unit:
            if re.search(r"crore|cr", unit, re.I): mul = 1e7
            elif re.search(r"lakh|lac|\bl\b", unit, re.I): mul = 1e5
        salary_m = num * mul
    # explicit "salary" mention
    m = re.search(rf"salary\s*(?:is|=)?\s*{_CURRENCY}({_NUM})", t, re.I)
    if m and salary_m is None:
        salary_m = float(m.group(1).replace(",", ""))

    # expenses
    m = re.search(rf"expenses?\s*(?:is|=)?\s*{_CURRENCY}({_NUM})", t, re.I)
    if m:
        expenses_m = float(m.group(1).replace(",", ""))

    # monthly investment
    monthly_investment = None
    for m in re.finditer(rf"{_CURRENCY}({_NUM})\s*(lakh|lac|l|crore|cr)?\s*{_PER_MONTH}", t, re.I):
        num = float(m.group(1).replace(",", ""))
        unit = m.group(2)
        mul = 1.0
        if unit:
            if re.search(r"crore|cr", unit, re.I): mul = 1e7
            elif re.search(r"lakh|lac|\bl\b", unit, re.I): mul = 1e5
        monthly_investment = num * mul

    # heuristics to map amounts to roles
    goal_amount = None
    loan_amount = None

    if "emi" in t or "loan" in t:
        loan_amount = amounts[0] if amounts else None
    else:
        # goal amount first if "save", "goal", etc.
        if "save" in t or "goal" in t or "target" in t:
            goal_amount = amounts[0] if amounts else None

    return {
        "amount": loan_amount,
        "interest_rate": rate,
        "tenure_years": years,
        "tenure_months": months,
        "salary_monthly": salary_m,
        "expenses_monthly": expenses_m,
        "goal_amount": goal_amount,
        "monthly_investment": monthly_investment,
    }
