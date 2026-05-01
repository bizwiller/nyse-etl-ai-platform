from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import pandas as pd

PathLike = Union[str, Path]


def read_parquet_file(parquet_path: PathLike, columns: Optional[List[str]] = None) -> pd.DataFrame:
    """Read a Parquet file into a pandas DataFrame."""
    parquet_path = Path(parquet_path)
    return pd.read_parquet(parquet_path, columns=columns)


def _make_json_serializable(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Convert DataFrame to JSON-serializable list of dictionaries."""
    records = df.to_dict(orient="records")
    # Convert all values to JSON-serializable types
    for record in records:
        for key, value in record.items():
            if pd.isna(value):
                record[key] = None
            elif isinstance(value, (pd.Timestamp, pd.Timedelta)):
                record[key] = str(value)
            elif isinstance(value, (int, float)):
                record[key] = float(value) if pd.notna(value) else None
    return records


def parquet_to_records(parquet_path: PathLike, columns: Optional[List[str]] = None, n_rows: Optional[int] = None) -> List[Dict[str, Any]]:
    """Read a Parquet file and return row records for frontend display.

    Args:
        parquet_path: Path to the Parquet file.
        columns: Optional list of columns to include.
        n_rows: Optional limit on number of rows to return.

    Returns:
        A list of dictionary records, which is JSON-serializable.
    """
    df = read_parquet_file(parquet_path, columns=columns)
    if n_rows is not None:
        df = df.head(n_rows)
    return _make_json_serializable(df)


def parquet_preview(parquet_path: PathLike, n_rows: int = 20) -> Dict[str, Any]:
    """Return a preview of a Parquet file for display."""
    df = read_parquet_file(parquet_path)
    preview_df = df.head(n_rows)
    return {
        "path": str(Path(parquet_path).resolve()),
        "rows": int(len(df)),
        "columns": list(df.columns),
        "preview": _make_json_serializable(preview_df),
    }
