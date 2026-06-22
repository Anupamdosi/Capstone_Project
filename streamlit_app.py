"""Streamlit chatbot UI for loan approval system."""

import streamlit as st
import requests
import json
from datetime import datetime
from database import get_statistics, get_decision_distribution, get_risk_scores, get_all_applications, export_to_json, export_to_csv

st.set_page_config(page_title="Agentic AI Loan Approval", layout="wide")

# Custom styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 30px;
    }
    .status-approved {
        color: #28a745;
        font-weight: bold;
    }
    .status-rejected {
        color: #dc3545;
        font-weight: bold;
    }
    .status-review {
        color: #ffc107;
        font-weight: bold;
    }
    .result-box {
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        border-left: 5px solid;
    }
    .approved-box {
        background-color: #d4edda;
        border-color: #28a745;
    }
    .rejected-box {
        background-color: #f8d7da;
        border-color: #dc3545;
    }
    .review-box {
        background-color: #fff3cd;
        border-color: #ffc107;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>🏦 Agentic AI Intelligent Loan Approval System</h1>", unsafe_allow_html=True)

# Sidebar for configuration
with st.sidebar:
    st.header("Configuration")
    api_url = st.text_input("API URL", value="http://localhost:8000")
    st.divider()
    st.info("Submit loan applications for AI-powered analysis and approval decisions.")

# Create tabs
tab1, tab2, tab3 = st.tabs(["📝 Single Application", "📊 Batch Processing", "📈 Analytics"])

with tab1:
    st.subheader("Submit Loan Application")

    col1, col2 = st.columns(2)

    with col1:
        applicant_id = st.text_input("Applicant ID", value="APP-001")
        age = st.slider("Age", min_value=18, max_value=80, value=35)
        income = st.number_input("Annual Income ($)", min_value=20000.0, value=75000.0, step=5000.0)
        employment_type = st.selectbox("Employment Type", ["Employed", "Self-employed", "Business Owner", "Retired"])

    with col2:
        credit_score = st.slider("Credit Score", min_value=300, max_value=850, value=720)
        loan_amount = st.number_input("Loan Amount ($)", min_value=10000.0, value=250000.0, step=10000.0)
        tenure_months = st.slider("Tenure (months)", min_value=6, max_value=360, value=180)
        existing_liabilities = st.number_input("Existing Liabilities ($)", min_value=0.0, value=50000.0, step=5000.0)

    location = st.text_input("Location", value="New York")

    if st.button("🚀 Analyze Application", use_container_width=True):
        with st.spinner("Analyzing application..."):
            try:
                payload = {
                    "applicant_id": applicant_id,
                    "age": age,
                    "income": income,
                    "employment_type": employment_type,
                    "credit_score": credit_score,
                    "loan_amount": loan_amount,
                    "tenure_months": tenure_months,
                    "existing_liabilities": existing_liabilities,
                    "location": location
                }

                response = requests.post(
                    f"{api_url}/analyze_loan_application",
                    json=payload,
                    timeout=10
                )

                if response.status_code == 200:
                    result = response.json()

                    # Determine styling
                    decision = result["decision"]
                    if decision == "Approved":
                        box_class = "approved-box"
                        status_class = "status-approved"
                    elif decision == "Rejected":
                        box_class = "rejected-box"
                        status_class = "status-rejected"
                    else:
                        box_class = "review-box"
                        status_class = "status-review"

                    st.markdown(f"""
                    <div class='result-box {box_class}'>
                        <h3 style='margin-top: 0;'>Decision: <span class='{status_class}'>{decision}</span></h3>
                        <p><strong>Risk Score:</strong> {result['risk_score']}/100</p>
                        <p><strong>Confidence Level:</strong> {result['confidence_level']}</p>
                        <p><strong>Case ID:</strong> {result['case_id']}</p>
                        <p><strong>Timestamp:</strong> {result['timestamp']}</p>
                        <p><strong>Explanation:</strong> {result['explanation']}</p>
                    </div>
                    """, unsafe_allow_html=True)

                    # Store result in session
                    if 'results' not in st.session_state:
                        st.session_state.results = []
                    st.session_state.results.append(result)

                else:
                    st.error(f"API Error: {response.status_code} - {response.text}")

            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to API. Make sure FastAPI service is running on http://localhost:8000")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

with tab2:
    st.subheader("Batch Processing")
    st.info("Upload a JSON file with multiple loan applications for batch processing.")

    uploaded_file = st.file_uploader("Choose JSON file", type="json")

    if uploaded_file and st.button("Process Batch", use_container_width=True):
        try:
            applications = json.load(uploaded_file)
            if not isinstance(applications, list):
                st.error("JSON must be an array of applications")
            else:
                with st.spinner(f"Processing {len(applications)} applications..."):
                    response = requests.post(
                        f"{api_url}/batch_analyze",
                        json=applications,
                        timeout=30
                    )

                    if response.status_code == 200:
                        results = response.json()
                        approved_count = sum(1 for r in results if r.get("status") == "success" and r.get("data", {}).get("decision") == "Approved")
                        rejected_count = sum(1 for r in results if r.get("status") == "success" and r.get("data", {}).get("decision") == "Rejected")
                        review_count = sum(1 for r in results if r.get("status") == "success" and r.get("data", {}).get("decision") == "Requires Manual Review")

                        col1, col2, col3, col4 = st.columns(4)
                        col1.metric("Total Processed", len(results))
                        col2.metric("Approved", approved_count)
                        col3.metric("Rejected", rejected_count)
                        col4.metric("Manual Review", review_count)

                        st.divider()
                        st.subheader("Batch Results")
                        for i, result in enumerate(results):
                            if result.get("status") == "success":
                                data = result.get("data", {})
                                with st.expander(f"Application {i+1}: {data.get('decision')} (ID: {data.get('case_id', 'N/A')})"):
                                    st.json(data)
                            else:
                                st.warning(f"Application {i+1}: Error - {result.get('error')}")
                    else:
                        st.error(f"API Error: {response.status_code}")

        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

with tab3:
    st.subheader("📊 Decision Analytics & History")

    # Get statistics from database
    stats = get_statistics()

    # Summary metrics from database
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Processed", stats['total_processed'])
    col2.metric("✅ Approved", stats['approved'])
    col3.metric("❌ Rejected", stats['rejected'])
    col4.metric("⚠️ Manual Review", stats['manual_review'])

    st.divider()

    # Average risk score
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Average Risk Score", f"{stats['average_risk_score']}/100")
    with col2:
        approval_rate = (stats['approved'] / stats['total_processed'] * 100) if stats['total_processed'] > 0 else 0
        st.metric("Approval Rate", f"{approval_rate:.1f}%")

    st.divider()

    # Risk score distribution from database
    st.subheader("📈 Risk Score Distribution")
    risk_scores = get_risk_scores()
    if risk_scores:
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        ax.hist(risk_scores, bins=10, color='steelblue', edgecolor='black')
        ax.set_xlabel("Risk Score")
        ax.set_ylabel("Frequency")
        ax.set_title("Distribution of Risk Scores (All Time)")
        st.pyplot(fig)
    else:
        st.info("No data yet. Submit applications to see charts.")

    st.divider()

    # Decision breakdown pie chart
    st.subheader("📊 Decision Breakdown")
    decisions = get_decision_distribution()

    if decisions:
        col1, col2 = st.columns(2)
        with col1:
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(8, 6))

            # Define colors for each decision type
            colors_map = {
                'Approved': '#28a745',              # Green ✅
                'Rejected': '#dc3545',              # Red ❌
                'Requires Manual Review': '#ffc107' # Orange ⚠️
            }

            # Get colors in the same order as decisions
            colors = [colors_map.get(decision, '#808080') for decision in decisions.keys()]

            ax.pie(decisions.values(), labels=decisions.keys(), autopct='%1.1f%%', startangle=90, colors=colors)
            ax.set_title("Decision Distribution")
            st.pyplot(fig)

        with col2:
            st.table({"Decision": list(decisions.keys()), "Count": list(decisions.values())})
    else:
        st.info("No decisions yet. Submit applications to see breakdown.")

    st.divider()

    # Export options
    st.subheader("💾 Export Data")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("📥 Export to JSON"):
            json_file = export_to_json()
            if json_file:
                with open(json_file, 'r') as f:
                    st.download_button(
                        label="Download JSON",
                        data=f.read(),
                        file_name=json_file,
                        mime="application/json"
                    )
                st.success(f"✅ Exported to {json_file}")

    with col2:
        if st.button("📥 Export to CSV"):
            csv_file = export_to_csv()
            if csv_file:
                with open(csv_file, 'r') as f:
                    st.download_button(
                        label="Download CSV",
                        data=f.read(),
                        file_name=csv_file,
                        mime="text/csv"
                    )
                st.success(f"✅ Exported to {csv_file}")

    st.divider()

    # Application history
    st.subheader("📋 Application History")
    applications = get_all_applications(limit=20)

    if applications:
        st.write(f"Showing latest {len(applications)} applications")
        for app in applications:
            with st.expander(f"📌 {app['applicant_id']} - {app['decision']} (Risk: {app['risk_score']}/100)"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Case ID:** {app['case_id']}")
                    st.write(f"**Decision:** {app['decision']}")
                    st.write(f"**Risk Score:** {app['risk_score']}/100")
                    st.write(f"**Confidence:** {app['confidence_level']}")
                with col2:
                    st.write(f"**Age:** {app['age']}")
                    st.write(f"**Income:** ${app['income']:,.0f}")
                    st.write(f"**Credit Score:** {app['credit_score']}")
                    st.write(f"**Loan Amount:** ${app['loan_amount']:,.0f}")
                st.write(f"**Explanation:** {app['explanation']}")
                st.write(f"**Timestamp:** {app['timestamp']}")
    else:
        st.info("No applications processed yet.")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; margin-top: 30px;'>
    <p><strong>Agentic AI Loan Approval System</strong> | Powered by Claude & LangGraph</p>
    <p>Multi-Agent Architecture with FastAPI & Streamlit</p>
</div>
""", unsafe_allow_html=True)
