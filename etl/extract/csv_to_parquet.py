from pathlib import Path
from typing import Optional, Union

import pandas as pd

PathLike = Union[str, Path]


def csv_to_parquet(csv_path: PathLike, parquet_path: Optional[PathLike] = None, index: bool = False, engine: str = "pyarrow") -> Path:
    """Convert a CSV file to Parquet format.

    Args:
        csv_path: Path to the source CSV file.
        parquet_path: Optional path for the output Parquet file. If omitted,
            uses the same base filename with a .parquet extension.
        index: Whether to include the DataFrame index in the Parquet file.
        engine: Parquet engine to use (pyarrow or fastparquet).

    Returns:
        Path to the written Parquet file.
    """
    csv_path = Path(csv_path)
    if parquet_path is None:
        parquet_path = csv_path.with_suffix(".parquet")
    else:
        parquet_path = Path(parquet_path)

    df = pd.read_csv(csv_path)
    df.to_parquet(parquet_path, index=index, engine=engine)
    return parquet_path
