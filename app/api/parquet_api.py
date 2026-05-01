from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from typing import List, Optional
import yfinance as yf
import pandas as pd
from etl.extract.parquet_viewer import parquet_preview, parquet_to_records
from etl.extract.csv_to_parquet import csv_to_parquet

app = FastAPI(title="Parquet Data API", version="1.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
DATA_DIR = Path(__file__).resolve().parents[2] / "data"


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


@app.get("/files")
def list_parquet_files():
    """List all available parquet files."""
    files = sorted([f.name for f in DATA_DIR.glob("*.parquet")])
    return {"files": files, "count": len(files)}


@app.get("/preview/{filename}")
def get_preview(filename: str, n_rows: int = Query(20, ge=1, le=1000)):
    """Get preview of a parquet file."""
    file_path = DATA_DIR / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"File not found: {filename}")

    if not file_path.suffix == ".parquet":
        raise HTTPException(status_code=400, detail="Only .parquet files are supported")

    try:
        preview = parquet_preview(file_path, n_rows=n_rows)
        return preview
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/data/{filename}")
def get_data(filename: str, n_rows: Optional[int] = Query(None, ge=1, le=10000)):
    """Get all data from a parquet file as JSON records."""
    file_path = DATA_DIR / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"File not found: {filename}")

    if not file_path.suffix == ".parquet":
        raise HTTPException(status_code=400, detail="Only .parquet files are supported")

    try:
        records = parquet_to_records(file_path, n_rows=n_rows)
        return {"data": records, "count": len(records)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/columns/{filename}")
def get_columns(filename: str):
    """Get column names from a parquet file."""
    file_path = DATA_DIR / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"File not found: {filename}")

    try:
        preview = parquet_preview(file_path, n_rows=1)
        return {"columns": preview["columns"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/fetch-ticker/{ticker}")
def fetch_ticker(ticker: str, period: str = Query("1mo", description="Period: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max")):
    """Fetch stock data for a ticker and save as parquet."""
    ticker_upper = ticker.upper().strip()
    
    if not ticker_upper:
        raise HTTPException(status_code=400, detail="Ticker symbol cannot be empty")
    
    if len(ticker_upper) > 5:
        raise HTTPException(status_code=400, detail="Ticker symbol too long (max 5 characters)")
    
    try:
        # Download data from yfinance
        df = yf.download(ticker_upper, period=period, progress=False)
        
        if df.empty:
            raise HTTPException(status_code=404, detail=f"No data found for ticker: {ticker_upper}")
        
        # Save as CSV first, then convert to parquet
        csv_path = DATA_DIR / f"{ticker_upper}_data.csv"
        df.to_csv(csv_path)
        
        # Convert to parquet
        parquet_path = csv_to_parquet(csv_path)
        
        # Clean up CSV
        csv_path.unlink()
        
        # Return preview of the newly created parquet file
        preview = parquet_preview(parquet_path, n_rows=20)
        preview["filename"] = parquet_path.name
        preview["message"] = f"Successfully fetched {len(df)} rows for {ticker_upper}"
        
        return preview
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching ticker data: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
