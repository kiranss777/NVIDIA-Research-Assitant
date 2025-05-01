# AI Use Disclosure

## Overview
This document provides a clear explanation of which AI tools are integrated into this project, how they are used, and the ethical and security considerations we have taken into account. Our goal is to ensure all stakeholders are fully informed about the AI components at work and the implications of their usage.

---

## AI Tools and Services

1. **LangChain / LangGraph**  
   - **Purpose**: Orchestrates multi-agent systems and LLM-based workflows.  
   - **Usage**: Routes queries to the appropriate agent (RAG, Snowflake, or Web Search) and composes the final user-facing response.  
   - **Data Handled**: User questions, context from retrieved text, and structured data from Snowflake.

2. **OpenAI GPT Models**  
   - **Purpose**: Natural language processing (NLP) to generate human-like text responses.  
   - **Usage**: Processes user questions, refines retrieved text, and produces summarized or synthesized output.  
   - **Data Handled**: Potentially personal or confidential data in user queries (depending on usage context), along with internal data from chunked documents used for retrieval-augmented generation.

3. **Anthropic Claude (Optional)**  
   - **Purpose**: Another large language model for text generation and summarization.  
   - **Usage**: Serves as a fallback or alternative to OpenAI GPT for text-based tasks.  
   - **Data Handled**: Same category as GPT-based models—user queries and the text corpora from the RAG pipeline.

4. **Pinecone**  
   - **Purpose**: Vector database hosting embeddings for chunked text (e.g., NVIDIA quarterly reports).  
   - **Usage**: Stores document embeddings and metadata (Year, Quarter). Used for similarity-based retrieval of relevant document chunks.  
   - **Data Handled**: Text embeddings of unstructured corporate disclosures, financial data, and user queries.

5. **Tavily / Web Search**  
   - **Purpose**: Provides real-time search results from external APIs for the latest news or publicly available data.  
   - **Usage**: Queries Tavily (or an alternative search API) to supplement up-to-date insights and trends about NVIDIA or related topics.  
   - **Data Handled**: User-provided search strings and public search results from external sources.

6. **Snowflake**  
   - **Purpose**: Stores structured financial data (valuation measures).  
   - **Usage**: The Snowflake agent queries the `NVIDIA_FINANCIALS` table to retrieve relevant structured data for numeric insights and charts.  
   - **Data Handled**: Officially sourced, structured financial metrics (e.g., Market Cap, P/E Ratio).

---

## Nature of Data Processed
- **User Queries**: May contain personal or proprietary information if inadvertently provided by the user.  
- **Company Data**: Project processes text from corporate disclosures (e.g., NVIDIA quarterly reports) and corresponding financial data.  
- **Search Results**: Real-time data retrieved by web search APIs (news headlines, articles, etc.).

All of this data may be temporarily handled by LLMs or stored in vector form in Pinecone.  
**No personally identifiable information (PII)** is intentionally collected, stored, or processed—unless inadvertently included by the user in their prompt or within the unstructured content.

---

## Ethical Considerations

1. **Data Privacy & Confidentiality**  
   - We avoid storing sensitive PII in Pinecone or any LLM service.  
   - Snowflake data is governed by existing database security protocols.

2. **Bias and Hallucination**  
   - Large Language Models can generate biased or incorrect outputs.  
   - We advise users to validate critical information against reliable sources.  
   - High-stakes or regulatory decisions should not rely solely on LLM outputs.

3. **Transparency**  
   - Users are informed that prompts and partial data sets may be processed by third-party AI models.  
   - Certain queries may be transmitted to external APIs.

4. **Monitoring and Logs**  
   - If logging is enabled, user prompts and AI responses may appear in logs.  
   - Logs are secured and purged according to data retention policies.

5. **Security**  
   - All external calls to Pinecone, OpenAI, or Tavily occur over HTTPS.  
   - Snowflake connections rely on secure protocols (TLS/SSL).  
   - Environment variables and credentials are restricted to authorized personnel only.

---

## User Consent
- By using this system, the user consents to having their queries processed by AI services.  
- If a more formal acceptance is required, link to a Terms of Service or Privacy Policy.

---

## Disclaimers

1. **No Investment Advice**  
   - Summaries or valuations provided by the system do not constitute investment advice.  
   - Consult a qualified financial professional before making any significant decisions.

2. **Accuracy and Reliability**  
   - The system may provide incorrect or outdated information.  
   - Users are responsible for verifying critical data independently.

3. **Third-Party Services**  
   - We rely on external providers (LLMs, search APIs, vector DB), whose availability is outside our control.  
   - Providers may impose rate limits or usage-based fees that could affect performance.

---

## Revisions and Updates
This document is subject to change as our AI integrations evolve. Any major changes will be accompanied by an update to **AIUseDisclosure.md**.

_Last Updated: [Date]_
