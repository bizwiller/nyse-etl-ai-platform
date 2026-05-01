# Frontend Options for Parquet Data Viewer

Three different GUI pages to view and explore parquet files from the ETL pipeline.

## 1. Streamlit App (Fastest to Deploy)

**Best for:** Quick prototyping, interactive Python UI, data exploration

### Start the app:
```bash
cd nyse-etl-ai-platform
streamlit run app/frontend/streamlit_app.py
```

**URL:** http://localhost:8501

**Features:**
- File selector dropdown
- Adjustable row count slider
- File info cards (total rows, columns, file size)
- Data preview table
- Download as CSV

### Requirements:
- Streamlit is already in `requirements.txt`

---

## 2. FastAPI + HTML (Web-Ready)

**Best for:** Production deployment, REST API, custom frontend integration

### Start the API:
```bash
cd nyse-etl-ai-platform
python -m app.api.parquet_api
```

**API URL:** http://localhost:8000
**API Docs:** http://localhost:8000/docs (Swagger UI)

### Open the HTML frontend:
```bash
# Option 1: Open in VS Code
code app/frontend/index.html

# Option 2: Open in browser
# Windows: start app/frontend/index.html
# Mac: open app/frontend/index.html
# Linux: xdg-open app/frontend/index.html
```

**Features:**
- Beautiful modern UI with gradient background
- File dropdown selector
- Row count input
- Info cards (total rows, columns, displayed rows)
- Data table with hover effects
- Responsive design

### API Endpoints:
- `GET /health` - Health check
- `GET /files` - List all parquet files
- `GET /preview/{filename}?n_rows=20` - Get file preview
- `GET /data/{filename}?n_rows=1000` - Get all data as JSON records
- `GET /columns/{filename}` - Get column names

---

## 3. Combined (FastAPI + Streamlit)

**Best for:** Having both options running simultaneously

### Start both:
```bash
cd nyse-etl-ai-platform
python app/frontend/run_frontend.py both
```

Or run them separately in different terminals:

**Terminal 1 - API:**
```bash
python -m app.api.parquet_api
```

**Terminal 2 - Streamlit:**
```bash
streamlit run app/frontend/streamlit_app.py
```

**URLs:**
- Streamlit: http://localhost:8501
- FastAPI: http://localhost:8000
- API Docs: http://localhost:8000/docs
- HTML Frontend: Open `app/frontend/index.html`

---

## Quick Start Commands

```bash
# Option 1: Streamlit only
python app/frontend/run_frontend.py streamlit

# Option 2: FastAPI only
python app/frontend/run_frontend.py fastapi

# Option 3: Both
python app/frontend/run_frontend.py both
```

---

## File Structure

```
app/
├── api/
│   ├── __init__.py
│   └── parquet_api.py          # FastAPI server
├── frontend/
│   ├── __init__.py
│   ├── streamlit_app.py        # Streamlit app
│   ├── index.html              # HTML frontend
│   └── run_frontend.py         # Launcher script
└── chatbot/
    └── (future)
```

---

## Testing the Data

Before using the frontends, make sure parquet files exist:

```bash
python -m etl.extract.test_yfinance
```

This generates `data/IONQ_sample.parquet` which will appear in all three interfaces.

---

## Troubleshooting

### Port already in use
- Streamlit: Change port with `streamlit run ... --server.port 8502`
- FastAPI: Modify port in `app/api/parquet_api.py`

### CORS issues with HTML frontend
- The HTML frontend makes requests to `http://localhost:8000`
- Ensure the FastAPI server is running on port 8000
- The FastAPI app includes CORS headers for all origins

### File not found errors
- Ensure `data/IONQ_sample.parquet` exists
- Run `python -m etl.extract.test_yfinance` to generate it
- Check that the working directory is `nyse-etl-ai-platform`
