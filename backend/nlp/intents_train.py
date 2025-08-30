
# Trains a simple intent classifier on synthetic finance queries.
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import os

DATA = [
    # loan_emi
    ("EMI for 10 lakh at 9% for 5 years", "loan_emi"),
    ("calculate emi 5L 8.5% 60 months", "loan_emi"),
    ("home loan emi 25L 20 years 7.2 percent", "loan_emi"),
    ("car loan 8 lakh 5 years interest 10%", "loan_emi"),
    ("what will be the monthly emi for 12lakh at 12 percent for 6 years", "loan_emi"),
    ("loan amount 9L, rate 11%, tenure 4 years, emi?", "loan_emi"),

    # savings_projection
    ("Can I save 5L in 2 years with salary 50k per month?", "savings_projection"),
    ("salary 80,000 per month, expenses 45,000, how much can I save in 18 months", "savings_projection"),
    ("target 3 lakh in one year, possible with 60k salary?", "savings_projection"),
    ("how much can I save in 24 months if salary is 70k", "savings_projection"),
    ("I want to reach 10L goal in 36 months", "savings_projection"),

    # investment_growth
    ("If I invest 10k monthly at 12% for 10 years how much will I get", "investment_growth"),
    ("SIP 5000 per month for 5 years at 10%", "investment_growth"),
    ("future value of 2000 monthly with 8 percent for 7 years", "investment_growth"),
    ("invest 15000 per month at 14 percent for 15 years", "investment_growth"),
    ("how much will my sip of 3000 monthly grow in 8 years at 12%", "investment_growth"),
]

def train_and_save(out_dir: str):
    texts = [t for t, y in DATA]
    labels = [y for t, y in DATA]
    X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=42, stratify=labels)
    pipe = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1,2), lowercase=True)),
        ("clf", LogisticRegression(max_iter=200)),
    ])
    pipe.fit(X_train, y_train)
    y_pred = pipe.predict(X_test)
    print(classification_report(y_test, y_pred))
    os.makedirs(out_dir, exist_ok=True)
    joblib.dump(pipe, os.path.join(out_dir, "intent_model.pkl"))
    print("Saved intent_model.pkl")

if __name__ == "__main__":
    here = os.path.dirname(__file__)
    train_and_save(here)
