
from fastapi import APIRouter
from pydantic import BaseModel
from finance.calculators import calculate_emi, future_value_sip, future_value_lumpsum

router = APIRouter(tags=["finance"])

class EMIRequest(BaseModel):
    amount: float
    annual_rate: float
    years: float

@router.post("/emi")
def emi(req: EMIRequest):
    emi_value, schedule = calculate_emi(req.amount, req.annual_rate, req.years)
    return {"emi": emi_value, "schedule": schedule}

class SIPRequest(BaseModel):
    monthly: float
    annual_rate: float
    years: float

@router.post("/sip")
def sip(req: SIPRequest):
    fv, series = future_value_sip(req.monthly, req.annual_rate, req.years)
    return {"future_value": fv, "series": series}

class LumpsumRequest(BaseModel):
    principal: float
    annual_rate: float
    years: float

@router.post("/lumpsum")
def lumpsum(req: LumpsumRequest):
    fv, series = future_value_lumpsum(req.principal, req.annual_rate, req.years)
    return {"future_value": fv, "series": series}
