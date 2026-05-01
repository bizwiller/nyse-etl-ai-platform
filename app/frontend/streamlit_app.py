import streamlit as st
from pathlib import Path
import pandas as pd
from etl.extract.parquet_viewer import parquet_preview, parquet_to_records

st.set_page_config(page_title="Parquet Data Viewer", layout="wide")

# Display method identifier
st.markdown("## 🎯 Streamlit App (Python Interactive UI)")
st.divider()

st.title("📊 Parquet Data Viewer")
st.markdown("View and explore parquet files from the ETL pipeline")

data_dir = Path(__file__).resolve().parents[2] / "data"

# File selector
parquet_files = sorted([f.name for f in data_dir.glob("*.parquet")])

if not parquet_files:
    st.warning("No parquet files found in the data directory")
else:
    selected_file = st.selectbox("Select a parquet file:", parquet_files)
    file_path = data_dir / selected_file

    if file_path.exists():
        col1, col2 = st.columns([2, 1])

        with col1:
            n_rows = st.slider("Rows to display:", 5, 100, 20)

        with col2:
            st.metric("File", selected_file)

        # Get preview data
        preview = parquet_preview(file_path, n_rows=n_rows)

        st.subheader("File Info")
        info_cols = st.columns(3)
        with info_cols[0]:
            st.metric("Total Rows", preview["rows"])
        with info_cols[1]:
            st.metric("Columns", len(preview["columns"]))
        with info_cols[2]:
            st.metric("File Size", f"{file_path.stat().st_size / 1024:.2f} KB")

        st.subheader("Columns")
        st.write(", ".join(preview["columns"]))

        st.subheader("Data Preview")
        df_preview = pd.DataFrame(preview["preview"])
        st.dataframe(df_preview, use_container_width=True)

        # Export options
        st.subheader("Export")
        if st.button("Download as CSV"):
            csv = df_preview.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"{Path(selected_file).stem}.csv",
                mime="text/csv",
            )
