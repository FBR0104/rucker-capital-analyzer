
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
                else:
                    st.info("No fund names detected.")
            except Exception as e:
                st.error(f"PDF extraction error: {e}")
        else:
            st.warning("Only PDF files are currently supported for fund name extraction.")
