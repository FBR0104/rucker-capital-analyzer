
import streamlit as st

st.set_page_config(page_title="Rucker Capital Wealth Analyzer", layout="centered")
st.title("Rucker Capital Wealth Analyzer")
st.markdown("Upload your client's investment report and provide the following details.")

with st.form("input_form"):
    uploaded_file = st.file_uploader("📂 Upload Investment Report (PDF or Excel)", type=["pdf", "xlsx"])
    client_name = st.text_input("👤 Client Name")
    client_age = st.number_input("🎂 Client Age", min_value=18, max_value=100, value=60)
    risk_profile = st.selectbox("⚖️ Risk Profile", ["Conservative", "Balanced", "Aggressive"])
    return_expectation = st.text_input("🎯 Return Expectation (e.g., CPI+4%)", value="CPI+4%")
    minimum_return = st.number_input("📉 Minimum Acceptable Return (%)", min_value=0.0, max_value=100.0, value=7.0)
    submitted = st.form_submit_button("🔍 Analyze Portfolio")

if submitted:
    if not uploaded_file:
        st.warning("Please upload an investment report to continue.")
    else:
        st.success(f"Report uploaded for {client_name} ({client_age} y/o, {risk_profile})")
        st.markdown("📈 *Portfolio analysis and GPT benchmarking will be added in the next version...*")
        st.markdown("🧾 *Report generation in `.docx` will be included here.*")
