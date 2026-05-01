"""
Parquet Data Viewer - Frontend Options

This module provides three different ways to view parquet data:

1. STREAMLIT APP (Quickest for Python users)
   Command: streamlit run app/frontend/streamlit_app.py
   URL: http://localhost:8501
   
2. FASTAPI + HTML (Best for web integration)
   Command: python -m app.api.parquet_api
   Frontend: Open app/frontend/index.html in browser
   API Docs: http://localhost:8000/docs
   
3. COMBINED (Streamlit with FastAPI backend)
   Start both above simultaneously
"""

import subprocess
import sys
import time
from pathlib import Path


def run_streamlit():
    """Launch Streamlit app."""
    print("\n" + "="*60)
    print("🎯 Streamlit App (Python Interactive UI)")
    print("="*60)
    print("Starting Streamlit app...")
    print("URL: http://localhost:8501")
    print("="*60 + "\n")
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app/frontend/streamlit_app.py"])


def run_fastapi():
    """Launch FastAPI server."""
    print("\n" + "="*60)
    print("🎯 FastAPI + HTML (Production Web UI)")
    print("="*60)
    print("Starting FastAPI server...")
    print("API URL: http://localhost:8000")
    print("API Docs: http://localhost:8000/docs")
    print("HTML Frontend: Open app/frontend/index.html in browser")
    print("="*60 + "\n")
    subprocess.run([sys.executable, "-m", "app.api.parquet_api"])


def run_both():
    """Launch both FastAPI and Streamlit."""
    print("\n" + "="*80)
    print("🎯 Combined Launcher (Run Both)")
    print("="*80)
    print("\nStarting both services:\n")
    print("  1. FastAPI + HTML (Production Web UI)")
    print("     URL: http://localhost:8000")
    print("     HTML: app/frontend/index.html\n")
    print("  2. Streamlit App (Python Interactive UI)")
    print("     URL: http://localhost:8501\n")
    print("="*80 + "\n")

    import threading

    # Run FastAPI in a separate thread
    api_thread = threading.Thread(target=run_fastapi, daemon=True)
    api_thread.start()

    time.sleep(2)

    # Run Streamlit in main thread
    run_streamlit()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nUsage:")
        print("  python app/frontend/run_frontend.py streamlit   # Run Streamlit only")
        print("  python app/frontend/run_frontend.py fastapi     # Run FastAPI only")
        print("  python app/frontend/run_frontend.py both        # Run both")
    else:
        mode = sys.argv[1].lower()
        if mode == "streamlit":
            run_streamlit()
        elif mode == "fastapi":
            run_fastapi()
        elif mode == "both":
            run_both()
        else:
            print(f"Unknown mode: {mode}")
