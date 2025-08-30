
# Knowledge-Aware Personal Finance Chatbot

Full-stack project (FastAPI backend + Streamlit UI) that answers finance questions:
- EMI calculations
- Savings projection (ML + rules hybrid)
- Investment growth (SIP / lumpsum)

## Quick Start

### 1) Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate  # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
# Train intent classifier (synthetic data)
python nlp/intents_train.py
# (Optional) Train a savings regressor (coming soon). Fallback heuristic exists.
uvicorn app:app --reload
```

### 2) Frontend (Streamlit)
```bash
cd ../frontend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# If backend runs elsewhere, create .streamlit/secrets.toml with:
# API_BASE = "http://<host>:8000/api"
streamlit run streamlit_app.py
```

## Project Structure
```
backend/
  app.py
  api/
    chatbot.py
    finance.py
  nlp/
    __init__.py
    intents_train.py
    intent_model.pkl        # generated after training
    pipeline.py
    slots.py
  ml/
    __init__.py
    savings_model.py        # uses trained model if available, else fallback
  finance/
    __init__.py
    calculators.py
  tests/
    test_finance.py
    test_nlp.py
  requirements.txt

frontend/
  streamlit_app.py
  requirements.txt
```

## Notes
- The NLP pipeline uses a TF-IDF + Logistic Regression intent classifier (baseline) and regex-based slot extraction for amounts, rates, durations, and monthly markers.
- Savings projection uses a trained regressor if available; otherwise, a safe fallback rule is applied.
- Charts and tables are rendered in Streamlit.
```

