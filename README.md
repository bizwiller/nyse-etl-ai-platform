# nyse-etl-ai-platform
Educational ETL + AI analytics platform using NYSE-like public data.

## Project Architecture

This repository is built as a modular ETL platform with both Python and web frontends.

- `etl/` - ETL pipeline code, data conversion, and parquet readers.
  - `etl/extract/test_yfinance.py` - downloads stock data, writes CSV, converts to parquet.
  - `etl/extract/csv_to_parquet.py` - converts CSV files to parquet.
  - `etl/extract/parquet_viewer.py` - reads parquet files and returns JSON-friendly preview data.
  - `etl/config/config.py` - configuration values and data directory path.

- `app/` - frontend and API application code.
  - `app/api/parquet_api.py` - FastAPI backend for listing and previewing parquet files, plus ticker fetching.
  - `app/frontend/streamlit_app.py` - Streamlit UI for browsing parquet data locally.
  - `app/frontend/index.html` - browser-based HTML UI calling the FastAPI backend.
  - `app/frontend/run_frontend.py` - launcher script to run Streamlit, FastAPI, or both.

- `data/` - stores generated parquet files and data artifacts.

## How it works

1. `test_yfinance.py` downloads stock history using `yfinance`.
2. The data is written to a CSV and then converted to parquet.
3. `parquet_viewer.py` loads parquet files and creates preview records.
4. Frontends consume the preview data:
   - Streamlit reads parquet directly.
   - HTML frontend calls FastAPI endpoints.

## Run the project

### Generate sample data
```bash
cd nyse-etl-ai-platform
python -m etl.extract.test_yfinance
```

### Run Streamlit UI
```bash
streamlit run app/frontend/streamlit_app.py
```

### Run FastAPI backend
```bash
uvicorn app.api.parquet_api:app --host 0.0.0.0 --port 8000
```

### Open browser UI
Open `app/frontend/index.html` in your browser, or serve it from a local web server.

## Available endpoints

- `GET /health`
- `GET /files`
- `GET /preview/{filename}?n_rows=20`
- `GET /data/{filename}?n_rows=10000`
- `GET /columns/{filename}`
- `GET /fetch-ticker/{ticker}?period=1mo`

## Notes

- Streamlit runs on port `8501` by default.
- FastAPI runs on port `8000` by default.
- The HTML UI depends on the FastAPI backend.

## Deploy to Render (Free Tier)

This project can be deployed to Render using the included `render.yaml` configuration.

### Steps

1. Push your repo to GitHub.
2. Create a new Web Service on Render.
3. Connect your GitHub repo and select the `main` branch.
4. Render will use `render.yaml` and install dependencies from `requirements.txt`.
5. The app starts with:
   ```bash
   uvicorn app.api.parquet_api:app --host 0.0.0.0 --port $PORT
   ```

### What is deployed

- FastAPI backend at `/`
- Browser UI served from `/`
- API endpoints available under the same domain

### Notes for Render

- Render provides the runtime port in `$PORT`.
- The HTML frontend now uses relative paths, so it works on the deployed domain.
- Parquet data files are stored on the instance filesystem at `data/`.
