NYSE ETL + AI‑Enabled Analytics Platform
End‑to‑End Educational Project
A fully containerized, cloud‑ready, end‑to‑end data engineering and AI analytics platform built using publicly available NYSE‑like datasets.
This project demonstrates enterprise‑grade patterns including ingestion, transformation, multi‑cloud loading, analytics modeling, BI dashboards, and a RAG‑powered chatbot — all using free or open‑source tools.

Project goals
Build a realistic, production‑style ETL pipeline using free market data

Demonstrate multi‑cloud data loading (Azure + AWS)

Implement curated analytics tables and BI dashboards

Provide a front‑end GUI for data operations and reporting

Add a Retrieval‑Augmented Generation (RAG) chatbot for natural‑language analytics

Package everything in Docker for reproducibility and deployment

High‑level architecture
Data sources  
Kaggle, Stooq, Yahoo Finance (yfinance), Alpha Vantage free tier

Ingestion layer  
Python ETL scripts for historical and incremental loads

Transformation layer  
Cleaning, normalization, feature engineering (returns, volatility, moving averages)

Storage

Raw zone: ADLS Gen2, S3

Curated zone: Azure SQL Database, Redshift/Athena

Vector store: Qdrant or Chroma

Analytics  
DuckDB, dbt (optional), Superset/Metabase dashboards

Front‑end  
Streamlit GUI with:

Load Data buttons

Report generation

RAG chatbot interface

AI layer  
Embeddings + vector DB + hosted LLM endpoint

Deployment  
Docker + docker‑compose
Optional CI/CD via GitHub Actions

Repository structure
Code
nyse-etl-ai-platform/
  etl/
    extract/
    transform/
    load/
    config/
  app/
    api/
    chatbot/
    frontend/
  infra/
    docker/
  notebooks/
  data/
  requirements.txt
  README.md
ETL pipeline overview
Extraction
Bulk historical load from Kaggle/Stooq

Daily incremental load from Yahoo Finance or Alpha Vantage

Stored as Parquet in raw zone

Transformation
Standardized schema

Feature engineering:

Daily returns

Rolling volatility

Moving averages

Curated tables written to cloud warehouses

Loading
Azure: ADLS Gen2 + Azure SQL

AWS: S3 + Athena/Redshift

Vector DB: Qdrant/Chroma for embeddings

Front‑end GUI (Streamlit)
The GUI provides:

Data Operations

Load historical data

Load incremental data

Reports

Top movers

Volatility summaries

Sector performance

Chatbot

Natural‑language queries

RAG‑powered responses using vector search + LLM

RAG chatbot architecture
User submits a question

System determines intent

SQL queries executed if needed

Embeddings generated and matched in vector DB

LLM produces final answer with retrieved context

Supports queries like:

“Explain today’s top movers.”

“Compare AAPL and MSFT volatility.”

“Which sectors were most stable this year?”

Dockerized deployment
Each component runs in its own container:

ETL worker

FastAPI backend

Streamlit front‑end

Qdrant vector DB

docker-compose orchestrates the full stack.

Tech stack (free/community)
Python 3.11

pandas, numpy, yfinance, pyarrow

FastAPI, Streamlit

DuckDB, dbt (open source)

Superset or Metabase

Qdrant or Chroma

Docker, GitHub Actions

Implementation roadmap
Phase 0 — Setup
Environment, repo structure, data source selection

Phase 1 — Ingestion
Historical + incremental extraction, raw storage

Phase 2 — Transformation
Cleaning, feature engineering, curated tables

Phase 3 — Analytics & GUI
Dashboards + Streamlit interface

Phase 4 — RAG & Deployment
Vector DB, chatbot, Dockerization, CI/CD

How to use this repository
Clone the repo

Create a Python environment

Install dependencies

Configure .env with your API keys

Run ETL scripts or launch the Streamlit GUI

Start the full stack with Docker

License
This project is for educational and learning purposes only.
No financial advice or real‑time trading functionality is included.