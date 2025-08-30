
import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Personal Finance Chatbot", layout="wide")

API_BASE = "http://localhost:8000/api"


st.title("💬 Knowledge-Aware Personal Finance Chatbot")

with st.sidebar:
    st.header("Try Examples")
    if st.button("Loan EMI Example"):
        st.session_state['input'] = "EMI for 10 lakh at 9% for 5 years"
    if st.button("Savings Projection Example"):
        st.session_state['input'] = "Can I save 5L in 2 years with 80k per month salary and 30k expenses?"
    if st.button("Investment Growth (SIP)"):
        st.session_state['input'] = "If I invest 5000 monthly at 12% for 10 years how much will I get?"

user_input = st.text_input("Ask anything about EMI, savings, or investments:", key="input", value=st.session_state.get('input', ""))

col1, col2 = st.columns([1,1])

if st.button("Ask"):
    try:
        resp = requests.post(f"{API_BASE}/chat", json={"message": user_input}, timeout=20)
        data = resp.json()
        st.success(data.get("text", ""))

        chart = data.get("chart")
        if chart and chart.get("data"):
            df = pd.DataFrame(chart["data"])
            with col1:
                if chart["type"] == "emi_schedule":
                    st.subheader("EMI Schedule")
                    st.dataframe(df.head(12))
                    st.caption("First 12 months shown.")
                else:
                    st.subheader("Projection")
                    st.line_chart(df.set_index("month"))
            with col2:
                st.subheader("Raw Slots / Debug")
                st.json(data.get("debug"))
    except Exception as e:
        st.error(f"Error: {e}")

st.markdown("---")
st.write("Backend:", API_BASE)
st.caption("Run backend: `uvicorn app:app --reload` in the backend folder. Run UI: `streamlit run streamlit_app.py`")
