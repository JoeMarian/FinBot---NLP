
import os
import joblib
import numpy as np

MODEL_PATH = os.path.join(os.path.dirname(__file__), "savings_regressor.pkl")

def load_savings_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    # Fallback simple linear rule if model not trained
    class FallbackModel:
        def predict(self, X):
            # X: [salary_m, expenses_m, months]
            X = np.array(X)
            monthly_net = X[:,0] - X[:,1]
            return np.maximum(0, monthly_net) * X[:,2]
    return FallbackModel()

def predict_savings(model, salary_monthly: float, expenses_monthly: float, months: int) -> float:
    return float(model.predict([[salary_monthly, expenses_monthly, months]])[0])
