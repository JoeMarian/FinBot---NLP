
import math

def calculate_emi(principal: float, annual_rate: float, years: float):
    r = (annual_rate / 12.0) / 100.0
    n = int(round(years * 12))
    if r == 0:
        emi = principal / n
    else:
        emi = principal * r * (1 + r) ** n / ((1 + r) ** n - 1)
    balance = principal
    schedule = []
    for m in range(1, n + 1):
        interest = balance * r
        principal_component = emi - interest
        balance = max(0.0, balance - principal_component)
        schedule.append({
            "month": m,
            "emi": float(emi),
            "interest": float(interest),
            "principal": float(principal_component),
            "balance": float(balance)
        })
    return float(emi), schedule

def future_value_sip(monthly: float, annual_rate: float, years: float):
    r = (annual_rate / 12.0) / 100.0
    n = int(round(years * 12))
    if r == 0:
        fv = monthly * n
    else:
        fv = monthly * (((1 + r) ** n - 1) / r) * (1 + r)
    series = [{"month": i, "value": monthly * (((1 + r) ** i - 1) / r) * (1 + r) if r != 0 else monthly * i} for i in range(1, n + 1)]
    return float(fv), series

def future_value_lumpsum(principal: float, annual_rate: float, years: float):
    r = annual_rate / 100.0
    n = years
    fv = principal * ((1 + r) ** n)
    # monthly checkpoints for charting
    series = [{"month": m, "value": principal * ((1 + r) ** (m/12.0))} for m in range(1, int(round(years*12)) + 1)]
    return float(fv), series
