
import streamlit as st
import pandas as pd
from PyPDF2 import PdfReader

st.set_page_config(page_title="Rucker Capital Wealth Analyzer", layout="centered")
st.title("Rucker Capital Wealth Analyzer")
st.markdown("Upload your client's investment report and provide the following details.")

# Form input
with st.form("input_form"):
    uploaded_file = st.file_uploader("📂 Upload Investment Report (PDF or Excel)", type=["pdf", "xlsx"])
    client_name = st.text_input("👤 Client Name")
    client_age = st.number_input("🎂 Client Age", min_value=18, max_value=100, value=60)
    risk_profile = st.selectbox("⚖️ Risk Profile", ["Conservative", "Balanced", "Aggressive"])
    return_expectation = st.text_input("🎯 Return Expectation (e.g., CPI+4%)", value="CPI+4%")
    minimum_return = st.number_input("📉 Minimum Acceptable Return (%)", min_value=0.0, max_value=100.0, value=7.0)
    submitted = st.form_submit_button("🔍 Analyze Portfolio")

# Analysis placeholder
if submitted:
    if not uploaded_file:
        st.warning("Please upload an investment report to continue.")
    else:
        st.success(f"Report uploaded for {client_name} ({client_age} y/o, {risk_profile})")

        fund_names = []

        if uploaded_file.name.endswith(".pdf"):
            try:
                reader = PdfReader(uploaded_file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
                st.markdown("🧾 **Extracted text from PDF:**")
                st.text_area("Extracted Content", value=text[:1500] + "...", height=200)

                # Dummy extraction (to be replaced with real logic)
                for line in text.splitlines():
                    if any(x in line.lower() for x in ["fund", "equity", "balanced", "income", "portfolio"]):
                        fund_names.append(line.strip())

                fund_names = list(set(fund_names))[:10]  # Simulate extracted fund names

                st.markdown("📌 **Detected Unit Trusts (simulated):**")
                st.write(fund_names)

                st.markdown("📉 *Portfolio performance benchmarking and report generation will follow next...*")

            except Exception as e:
                st.error(f"Error reading PDF: {e}")
        else:
            st.warning("Excel support will be added next.")
