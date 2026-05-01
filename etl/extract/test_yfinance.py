from etl.config.config import DATA_DIR
from etl.extract.csv_to_parquet import csv_to_parquet
import yfinance as yf

def main():
    ticker = "IONQ"
    df = yf.download(ticker, period="1mo", interval="1d")
    DATA_DIR.mkdir(exist_ok=True)
    csv_out = DATA_DIR / f"{ticker}_sample.csv"
    df.to_csv(csv_out, index=False)
    print(f"Wrote {csv_out} with {len(df)} rows")

    parquet_out = csv_to_parquet(csv_out)
    print(f"Wrote {parquet_out} from {csv_out}")


if __name__ == "__main__":
    main()
