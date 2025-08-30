
from fastapi import APIRouter
from pydantic import BaseModel
from nlp.pipeline import NLPPipeline
from finance.calculators import calculate_emi, future_value_sip, future_value_lumpsum
from ml.savings_model import load_savings_model, predict_savings

router = APIRouter(tags=["chatbot"])

class ChatRequest(BaseModel):
    message: str

pipeline = NLPPipeline()
savings_model = load_savings_model()

@router.post("/chat")
def chat(req: ChatRequest):
    intent, slots, debug = pipeline.parse(req.message)

    response = {"intent": intent, "slots": slots, "debug": debug}

    try:
        if intent == "loan_emi":
            P = slots.get("amount")
            annual_rate = slots.get("interest_rate")
            years = slots.get("tenure_years") or (slots.get("tenure_months", 0) / 12.0)
            if P and annual_rate and years:
                emi, schedule = calculate_emi(P, annual_rate, years)
                response["text"] = f"EMI for ₹{int(P):,} at {annual_rate:.2f}% for {years:.2f} years is ₹{emi:,.2f}."
                response["chart"] = {"type": "emi_schedule", "data": schedule}
            else:
                response["text"] = "Please provide loan amount, annual interest rate, and tenure."
        elif intent == "savings_projection":
            salary_m = slots.get("salary_monthly")
            expenses_m = slots.get("expenses_monthly") or (0.6 * salary_m if salary_m else None)
            years = slots.get("tenure_years") or (slots.get("tenure_months", 0) / 12.0)
            goal = slots.get("goal_amount")
            if salary_m and years is not None:
                months = int(round(years * 12))
                pred = predict_savings(savings_model, salary_m, expenses_m or 0, months)
                txt = f"Projected savings over {months} months: ₹{pred:,.0f}."
                if goal:
                    txt += " " + ("✅ You can reach your goal." if pred >= goal else "⚠️ You may fall short of your goal.")
                response["text"] = txt
                response["chart"] = {"type": "savings_projection", "data": [{"month": i+1, "amount": (pred/months)*(i+1)} for i in range(months)]}
            else:
                response["text"] = "Please provide monthly salary (and optionally expenses) and duration."
        elif intent == "investment_growth":
            contrib = slots.get("monthly_investment")
            rate = slots.get("interest_rate") or 10.0
            years = slots.get("tenure_years") or (slots.get("tenure_months", 0) / 12.0)
            if contrib and years is not None:
                fv, series = future_value_sip(contrib, rate, years)
                response["text"] = f"Future value of ₹{contrib:,.0f}/month at {rate:.2f}% for {years:.2f} years: ₹{fv:,.0f}."
                response["chart"] = {"type": "investment_growth", "data": series}
            else:
                response["text"] = "Please provide monthly contribution and duration."
        else:
            response["text"] = "I can help with EMI, savings projections, and investment growth. Try: 'EMI for 10L at 9% for 5 years'."
    except Exception as e:
        response["text"] = f"Error while processing: {e}"
    return response
