from etl.extract.parquet_viewer import parquet_preview, parquet_to_records
from pathlib import Path

path = Path('data/IONQ_sample.parquet')
print(parquet_preview(path, n_rows=3))
print('---')
print(parquet_to_records(path, n_rows=2))
