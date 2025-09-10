# Multi-Agent Research Assistant 

An integrated research assistant that leverages three specialized agents to provide comprehensive, data-driven research reports on NVIDIA. This project combines a Snowflake Agent (for structured financial valuation data), a Pinecone-powered RAG Agent (for historical NVIDIA reports), and a Web Search Agent (for real-time insights) into one cohesive system orchestrated with LangGraph.

#Application URL:http://34.28.77.168:8501/
#Backend URL:http://34.28.77.168:8000/

#Demo Video:https://www.loom.com/share/e49782356b9e4166a6a05f40c66b6291?sid=5430a24b-edd1-4400-804d-8e07125b8d40

##Code Lab: https://codelabs-preview.appspot.com/?file_id=1puXxuXqOF42bGrze0aGEXMlsrtask7rusJ0M6XoU4oQ#0
## Overview

This project builds on our previous work (Assignment 4.2) to create an agentic multi-agent system that:
- **Snowflake Agent:** Connects to a Snowflake database to query structured valuation metrics sourced from Yahoo Finance.
- **RAG Agent:** Uses Pinecone to perform metadata-filtered retrieval from NVIDIA quarterly reports and generates context-aware responses.
- **Web Search Agent:** Fetches real-time industry insights using web search APIs (e.g., SerpAPI, Tavily, or Bing).

The integrated system produces research reports that include historical performance summaries, structured financial visuals, and up-to-date industry trends.

## Features

- **Multi-Agent Orchestration:** Coordinated responses from three specialized agents.
- **Hybrid Search:** Utilize Pinecone with structured metadata (Year & Quarter) for fine-tuned retrieval.
- **Real-Time Insights:** Leverage web search APIs to supplement reports with the latest news.
- **User-Friendly Interface:** Streamlit UI with FastAPI backend for research question input and filtering.
- **Dockerized Deployment:** Ready for cloud deployment with a streamlined Docker setup.

## Architecture

The system comprises:

1. **Streamlit Frontend**  
   - Collects user input (questions, year, quarter, and agent selection).  
   - Displays consolidated results (historical analysis, charts, real-time insights).

2. **FastAPI Backend**  
   - Receives requests from Streamlit at `/report` or other endpoints.  
   - Orchestrates calls to:
     - **RAG Agent** for Pinecone retrieval and LLM summarization.
     - **Snowflake Agent** to generate textual/visual summaries of numeric data.
     - **Web Agent** for real-time industry headlines.

3. **Data Sources**  
   - **Pinecone**: Stores chunked embedding vectors of NVIDIA reports, with year/quarter metadata.  
   - **Snowflake**: Holds structured financial data for NVIDIA.  
   - **Tavily / Web**: Provides real-time search results.


##Architectural diagram
![Editor _ Mermaid Chart-2025-03-28-210931](https://github.com/user-attachments/assets/b81d7565-6e0d-4843-a28c-8e00cb9eb13e)

Prerequisites
Python 3.9+

Pinecone account and index created (e.g. "bigdata5")

Snowflake account/database (table NVIDIA_FINANCIALS)

API keys for:

Snowflake (SNOWFLAKE_USER, SNOWFLAKE_PASSWORD, etc.)

Pinecone (PINECONE_API_KEY, PINECONE_REGION)

Tavily / SerpAPI (TAVILY_API_KEY, SERPAPI_API_KEY) for web search

OpenAI (OPENAI_API_KEY) if using GPT models

Docker (optional, if you plan to containerize)
Environment Setup
Create a .env file in your project root. An example:

bash
Copy
Edit
# Snowflake
SNOWFLAKE_USER="YOUR_SNOWFLAKE_USER"
SNOWFLAKE_PASSWORD="YOUR_SNOWFLAKE_PASSWORD"
SNOWFLAKE_ACCOUNT="YOUR_SNOWFLAKE_ACCOUNT"
SNOWFLAKE_DATABASE="YOUR_DB"
SNOWFLAKE_SCHEMA="YOUR_SCHEMA"
SNOWFLAKE_WAREHOUSE="YOUR_WAREHOUSE"
SNOWFLAKE_STAGE="YOUR_STAGE"

# Pinecone
PINECONE_API_KEY="YOUR_PINECONE_KEY"
PINECONE_REGION="YOUR_PINECONE_REGION"

# Web Search
TAVILY_API_KEY="YOUR_TAVILY_KEY"

# OpenAI
OPENAI_API_KEY="YOUR_OPENAI_API_KEY"

# Etc...
Note: Keep your .env private! Never commit API keys to a public repository.

Installation
Clone or Download the repository:

bash
Copy
Edit
git clone https://github.com/yourusername/nvidia-research-assistant.git
cd nvidia-research-assistant
Install Python Dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Make sure requirements.txt includes packages like fastapi, uvicorn, streamlit, langchain, sentence-transformers, pinecone-client, snowflake-connector-python, pydantic, etc.

Populate Snowflake (if not done already):

Ensure NVIDIA_FINANCIALS table is created.

Use scripts like quarterly.py or NVIDIA_Snowflake_conn.py to load CSV data.

Check Pinecone Index:

Confirm an index matching your config (INDEX_NAME = "bigdata5") is created in the Pinecone dashboard.

Make sure the dimension (e.g., 384 for all-MiniLM-L6-v2) matches your embedding model.
