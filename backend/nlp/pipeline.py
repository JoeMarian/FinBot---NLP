
import os
import joblib
from .slots import extract_slots

MODEL_PATH = os.path.join(os.path.dirname(__file__), "intent_model.pkl")

class NLPPipeline:
    def __init__(self):
        self.intent_model = joblib.load(MODEL_PATH) if os.path.exists(MODEL_PATH) else None

    def parse(self, text: str):
        intent = "unknown"
        if self.intent_model:
            intent = self.intent_model.predict([text])[0]
        else:
            # simple keyword fallback
            t = text.lower()
            if "emi" in t or "loan" in t: intent = "loan_emi"
            elif "save" in t or "goal" in t or "salary" in t: intent = "savings_projection"
            elif "sip" in t or "invest" in t or "future value" in t: intent = "investment_growth"

        slots = extract_slots(text)
        debug = {"model_loaded": self.intent_model is not None, "slots": slots}
        return intent, slots, debug
