# streamlit_app.py

import streamlit as st
import requests
import pandas as pd
import base64

# URL for the FastAPI report endpoint (adjust if running on a different host/port)
API_URL = "http://34.28.77.168:8000/report"

st.set_page_config(page_title="NVIDIA Research Assistant", layout="wide")
st.title("🔍 NVIDIA Multi-Agent Research Assistant")

st.markdown(
    """
    This integrated research assistant leverages three agents:
    - **Snowflake Agent:** Retrieves structured financial valuation metrics.
    - **RAG Agent:** Uses Pinecone with metadata filtering (Year/Quarter) for historical performance.
    - **Web Search Agent:** Fetches real-time industry insights.
    
    Enter your research question and select options to generate a comprehensive report.
    """
)

# --- UI Inputs ---
question = st.text_input("Enter your research question:")
year = st.selectbox("Year", [None] + list(range(2018, 2025)))
quarter = st.selectbox("Quarter", [None, 1, 2, 3, 4])
agents = st.multiselect("Include agents to run:", ["rag", "financial", "web"], default=["rag", "financial", "web"])

if st.button("Generate Report"):
    if not question:
        st.error("Please enter a research question.")
    else:
        payload = {
            "question": question,
            "year": year,
            "quarter": quarter,
            "include_agents": agents
        }
        with st.spinner("Generating report..."):
            response = requests.post(API_URL, json=payload)
        if response.status_code != 200:
            st.error(f"Error: {response.status_code} - {response.text}")
        else:
            report = response.json()
            # --- Display RAG (Historical) Output ---
            if "historical" in report:
                st.subheader("📜 Historical Performance (RAG)")
                st.write(report["historical"])

            # --- Display Financial Metrics ---
            if "financial_summary" in report:
                st.subheader("💰 Financial Valuation Metrics")
                if isinstance(report["financial_summary"], list):
                    df_fin = pd.DataFrame(report["financial_summary"])
                    st.dataframe(df_fin)
                    chart_b64 = report.get("financial_chart", "")
                    if chart_b64:
                        chart_bytes = base64.b64decode(chart_b64)
                        st.image(chart_bytes, caption="MarketCap Over Time", use_column_width=True)
                else:
                    st.write(report["financial_summary"])

            # --- Display Web Insights ---
            if "web" in report:
                st.subheader("🌐 Real-Time Industry Insights")
                if isinstance(report["web"], list) and report["web"]:
                    df_web = pd.DataFrame(report["web"])
                    st.dataframe(df_web)
                else:
                    st.write("No web insights available.")
