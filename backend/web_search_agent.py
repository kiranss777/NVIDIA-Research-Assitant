import os
import base64
import io
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt
from tavily import TavilyClient
# Load environment
load_dotenv()

# Import existing agents and helpers
from  rag_agent import rag_agent, build_graph, RAGState
from  langgraph_app import query_snowflake

app = FastAPI(title="NVIDIA Research Assistant API")

# Request models
class CombinedSearchRequest(BaseModel):
    question: str
    top_k: int = 500

class ReportRequest(BaseModel):
    question: str
    year: Optional[int]
    quarter: Optional[int]
    top_k: int = 500
    include_agents: List[str] = ["rag", "financial", "web"]

# Tavily Web Search using TavilyClient
def tavily_search(query: str, num_results: int = 10) -> list:
    api_key = os.environ.get("TAVILY_API_KEY")
    if not api_key:
        raise Exception("TAVILY_API_KEY is not set in the environment.")
    
    #api_key = "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"
    # Instantiate the Tavily client
    client = TavilyClient(api_key=api_key)
    response = client.search(query)
    # Assuming the response is a dictionary with a "results" key
    return response.get("results", [])

# Endpoints
@app.post("/report")
def research_report(req: ReportRequest):
    report = {}
    # RAG
    if "rag" in req.include_agents:
        state: RAGState = {"question": req.question, "top_k": req.top_k, "year": req.year, "quarter": req.quarter}
        rag_out = build_graph().invoke(state)
        report["historical"] = rag_out.get("rag_output", "No RAG output")
    # Snowflake
    if "financial" in req.include_agents and req.year and req.quarter:
        sql = f"SELECT * FROM NVIDIA_FINANCIALS WHERE YEAR(ASOFDATE)={req.year} AND QUARTER(ASOFDATE)={req.quarter}"
        df = query_snowflake(sql)
        report["financial_summary"] = df.to_dict(orient="records")
        buf = io.BytesIO()
        df.sort_values("ASOFDATE").plot(x="ASOFDATE", y="MARKETCAP", marker='o')
        plt.tight_layout()
        plt.savefig(buf, format="png")
        plt.close()
        report["financial_chart"] = base64.b64encode(buf.getvalue()).decode()
    # Web
    if "web" in req.include_agents:
        report["web"] = tavily_search(req.question)
    return report

@app.post("/combined")
def combined_search(request: CombinedSearchRequest):
    # RAG + Web
    state: RAGState = {"question": request.question, "top_k": request.top_k}
    rag_result = build_graph().invoke(state).get("rag_output")
    web_results = tavily_search(request.question)
    return {"rag_result": rag_result, "web_results": web_results}

@app.post("/rag")
def rag_endpoint(request: CombinedSearchRequest):
    state: RAGState = {"question": request.question, "top_k": request.top_k}
    return {"rag_result": build_graph().invoke(state).get("rag_output")}

@app.post("/web")
def web_search_endpoint(request: CombinedSearchRequest):
    return {"web_results": tavily_search(request.question)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
