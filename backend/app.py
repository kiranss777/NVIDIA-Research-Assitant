# app.py (located in the backend folder)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import io
import base64
import matplotlib.pyplot as plt
import pandas as pd

# Use relative imports because app.py is in the same package as the other modules.
from  rag_agent import build_graph
from  langgraph_app import query_snowflake
from  web_search_agent import tavily_search

app = FastAPI(title="NVIDIA Research Assistant API")

class ReportRequest(BaseModel):
    question: str
    year: Optional[int] = None
    quarter: Optional[int] = None
    include_agents: List[str] = ["rag", "financial", "web"]

def generate_report(question: str, year: Optional[int], quarter: Optional[int], agents: List[str]):
    report = {}

    # --- RAG Agent (Historical Performance) ---
    if "rag" in agents:
        state = {"question": question, "top_k": 500}
        if year is not None:
            state["year"] = year
        if quarter is not None:
            state["quarter"] = quarter
        graph = build_graph()
        result_state = graph.invoke(state)
        report["historical"] = result_state.get("rag_output", "No RAG output returned.")

    # --- Financial Metrics (Snowflake Agent) ---
    if "financial" in agents and year is not None and quarter is not None:
        sql = f"SELECT * FROM NVIDIA_FINANCIALS WHERE YEAR(ASOFDATE)={year} AND QUARTER(ASOFDATE)={quarter}"
        df_financial = query_snowflake(sql)
        if not df_financial.empty:
            report["financial_summary"] = df_financial.to_dict(orient="records")
            buf = io.BytesIO()
            df_sorted = df_financial.sort_values("ASOFDATE")
            ax = df_sorted.plot(x="ASOFDATE", y="MARKETCAP", marker='o')
            plt.tight_layout()
            plt.savefig(buf, format="png")
            plt.close()
            report["financial_chart"] = base64.b64encode(buf.getvalue()).decode()
        else:
            report["financial_summary"] = "No financial data found for the selected Year/Quarter."

    # --- Web Insights (Web Search Agent) ---
    if "web" in agents:
        web_results = tavily_search(question)
        report["web"] = web_results

    return report

@app.post("/report")
def get_report(request: ReportRequest):
    try:
        report = generate_report(request.question, request.year, request.quarter, request.include_agents)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
