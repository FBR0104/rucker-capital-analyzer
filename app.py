
import streamlit as st
import pandas as pd
from PyPDF2 import PdfReader
import re

st.set_page_config(page_title="Rucker Capital Wealth Analyzer", layout="centered")
st.title("Rucker Capital Wealth Analyzer")
st.markdown("Upload your client's investment report and provide the following details.")

# Form input
with st.form("input_form"):
    uploaded_file = st.file_uploader("📄 Upload Investment Report (PDF or Excel)", type=["pdf", "xlsx"])
    client_name = st.text_input("👤 Client Name")
    client_age = st.number_input("🎂 Client Age", min_value=18, max_value=100, value=60)
    risk_profile = st.selectbox("📉 Risk Profile", ["Conservative", "Balanced", "Aggressive"])
    return_expectation = st.text_input("🍒 Return Expectation (e.g., CPI+4%)", value="CPI+4%")
    minimum_return = st.number_input("📉 Minimum Acceptable Return (%)", min_value=0.0, max_value=100.0, value=7.0)
    submitted = st.form_submit_button("🔍 Analyze Portfolio")

# Analysis
if submitted:
    if not uploaded_file:
        st.warning("Please upload an investment report to continue.")
    else:
        st.success(f"Report uploaded for {client_name} ({client_age} y/o, {risk_profile})")

        if uploaded_file.name.endswith(".pdf"):
            try:
                reader = PdfReader(uploaded_file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()

                st.markdown("### 📄 Extracted Content")
                st.text_area("Extracted Text", text, height=200)

                # --- Fund Name Extraction Logic ---
                lines = text.split("\n")
                possible_fund_names = []
                for line in lines:
                    if any(keyword in line.lower() for keyword in ["fund", "equity", "income", "growth", "prescient", "stanlib", "coronation", "momentum"]):
                        cleaned = re.sub(r'[^\w\s\-&]', '', line).strip()
                        if 3 < len(cleaned) < 100:
                            possible_fund_names.append(cleaned)

                cleaned_fund_names = list(sorted(set(possible_fund_names)))

                if cleaned_fund_names:
                    st.markdown("### 📌 Cleaned Unit Trust Fund Names")
                    for fund in cleaned_fund_names:
                        st.markdown(f"- {fund}")
                            # --- Now match to benchmark CSV using fuzzy logic ---
    from rapidfuzz import fuzz
    import numpy as np

    try:
        benchmark_df = pd.read_csv("Wealth_Analyzer_Benchmarks.csv")  # must be uploaded into repo or fetched from Zapier later
        minimum_return_threshold = minimum_return

        matched_results = []
        for extracted in cleaned_fund_names:
            best_match = None
            best_score = 0

            for idx, row in benchmark_df.iterrows():
                score = fuzz.ratio(extracted.lower(), row['Fund Name'].lower())
                if score > best_score:
                    best_score = score
                    best_match = row

            if best_score > 80:
                result = {
                    "Extracted Fund Name": extracted,
                    "Matched Fund Name": best_match["Fund Name"],
                    "1Y Return": best_match["1Y Return"],
                    "3Y Return": best_match["3Y Return"],
                    "5Y Return": best_match["5Y Return"],
                    "Meets Benchmark (3Y)": "✅" if best_match["3Y Return"] >= minimum_return_threshold else "❌"
                }
            else:
                result = {
                    "Extracted Fund Name": extracted,
                    "Matched Fund Name": "❌ Not Found",
                    "1Y Return": np.nan,
                    "3Y Return": np.nan,
                    "5Y Return": np.nan,
                    "Meets Benchmark (3Y)": "⚠️"
                }

            matched_results.append(result)

        import pandas as pd
        df_results = pd.DataFrame(matched_results)
        st.markdown("### 📊 Benchmark Results (Fuzzy Matched)")
        st.dataframe(df_results)

    except Exception as e:
        st.error(f"Benchmark matching failed: {e}")

                else:
                    st.info("No fund names detected.")
            except Exception as e:
                st.error(f"PDF extraction error: {e}")
        else:
            st.warning("Only PDF files are currently supported for fund name extraction.")
