
# Simple trainer for a synthetic savings regressor.
import numpy as np, pandas as pd, joblib, os
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

def synth(n=5000, seed=7):
    rng = np.random.default_rng(seed)
    salary = rng.integers(20000, 200000, size=n)  # monthly
    expenses = (salary * rng.uniform(0.3, 0.9, size=n)).astype(float)
    months = rng.integers(6, 60, size=n)
    # true savings with some noise & inflation leakage
    leakage = rng.uniform(0.0, 0.15, size=n)
    y = np.maximum(0, (salary - expenses)) * months * (1 - leakage)
    X = np.c_[salary, expenses, months]
    return X, y

def main():
    X, y = synth()
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)
    m = LinearRegression()
    m.fit(Xtr, ytr)
    pred = m.predict(Xte)
    print("R2:", r2_score(yte, pred))
    out = os.path.join(os.path.dirname(__file__), "savings_regressor.pkl")
    joblib.dump(m, out)
    print("Saved", out)

if __name__ == "__main__":
    main()
