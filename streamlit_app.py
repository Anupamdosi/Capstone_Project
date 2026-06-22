"""Streamlit chatbot UI for TD Bank loan approval system."""

import streamlit as st
import requests
import json
import random
from datetime import datetime
from database import get_statistics, get_decision_distribution, get_risk_scores, get_all_applications, export_to_json, export_to_csv

# Helper functions
def generate_applicant_id():
    """Generate random applicant ID."""
    return f"APP-{random.randint(100000, 999999)}"

def convert_age_to_months(years: int, months: int) -> int:
    """Convert years and months to total months."""
    return years * 12 + months

st.set_page_config(page_title="TD Bank - Agentic Loan Approval", layout="wide")

# Custom styling with TD Bank theme
st.markdown("""
<style>
    /* Watermark */
    body::before {
        content: "TD BANK";
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%) rotate(-45deg);
        font-size: 120px;
        color: rgba(0, 51, 102, 0.08);
        font-weight: bold;
        z-index: -1;
        white-space: nowrap;
    }

    .main-header {
        text-align: center;
        color: #003366;
        margin-bottom: 10px;
        font-size: 2.5em;
        font-weight: 900;
        border-bottom: 4px solid #003366;
        padding-bottom: 20px;
    }

    .bank-subtitle {
        text-align: center;
        color: #666666;
        font-size: 1.1em;
        margin-bottom: 20px;
        font-style: italic;
    }

    .user-badge {
        background: linear-gradient(135deg, #003366 0%, #004d80 100%);
        color: white;
        padding: 12px 20px;
        border-radius: 8px;
        margin-bottom: 20px;
        text-align: center;
        font-weight: bold;
        border: 2px solid #003366;
    }

    .status-approved {
        color: #2d5016;
        font-weight: bold;
        font-size: 1.1em;
    }

    .status-rejected {
        color: #8B0000;
        font-weight: bold;
        font-size: 1.1em;
    }

    .status-review {
        color: #ff8c00;
        font-weight: bold;
        font-size: 1.1em;
    }

    .result-box {
        border-radius: 12px;
        padding: 25px;
        margin: 15px 0;
        border: 3px solid;
        box-shadow: 0 4px 8px rgba(0, 51, 102, 0.2);
        background: white;
    }

    .approved-box {
        background-color: #e8f5e9;
        border-color: #2d5016;
    }

    .rejected-box {
        background-color: #ffebee;
        border-color: #8B0000;
    }

    .review-box {
        background-color: #fff8e1;
        border-color: #ff8c00;
    }

    .form-container {
        border: 2px solid #003366;
        padding: 20px;
        border-radius: 10px;
        background-color: #f9fafb;
        margin-bottom: 20px;
    }

    .section-header {
        color: #003366;
        border-left: 5px solid #2d5016;
        padding-left: 15px;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 15px;
    }

    .footer-watermark {
        text-align: center;
        color: #999999;
        margin-top: 40px;
        padding-top: 20px;
        border-top: 2px solid #e0e0e0;
        font-size: 0.9em;
    }

    .tab-header {
        color: #003366;
        font-weight: bold;
        border-bottom: 3px solid #003366;
        padding-bottom: 10px;
    }

    .metric-card {
        border: 2px solid #003366;
        border-radius: 8px;
        padding: 15px;
        background-color: #f0f4f8;
    }
</style>
""", unsafe_allow_html=True)

# TD Bank Header with user info
col1, col2 = st.columns([4, 1])
with col1:
    st.markdown("<div class='main-header'>🏦 TD BANK</div>", unsafe_allow_html=True)
    st.markdown("<div class='bank-subtitle'>Intelligent Loan Approval System - Powered by AI</div>", unsafe_allow_html=True)
with col2:
    st.markdown("<div class='user-badge'>👤 User: Anupam</div>", unsafe_allow_html=True)

# Sidebar for configuration
with st.sidebar:
    st.markdown("---")
    st.markdown("### ⚙️ Configuration")
    st.markdown("---")
    api_url = st.text_input("API URL", value="http://localhost:8000")
    st.markdown("---")
    st.markdown("""
    <div style='background-color: #e8f5e9; padding: 15px; border-radius: 8px; border-left: 4px solid #2d5016;'>
    <strong style='color: #2d5016;'>✓ Success Indicator:</strong> Light Green
    <br><strong style='color: #8B0000;'>✗ Failure Indicator:</strong> Blood Red
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.info("💼 Submit loan applications for AI-powered analysis and approval decisions.")

# Create tabs
tab1, tab2, tab3 = st.tabs(["📝 Single Application", "📊 Batch Processing", "📈 Analytics Dashboard"])

with tab1:
    st.markdown("<div class='section-header'>📝 Loan Application Form</div>", unsafe_allow_html=True)

    st.markdown("<div class='form-container'>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📋 Applicant Information")

        # Applicant ID with regenerate button
        col_id1, col_id2 = st.columns([3, 1])
        with col_id1:
            applicant_id = st.text_input("Applicant ID", value=generate_applicant_id(), key="app_id")
        with col_id2:
            if st.button("🔄 New", key="regen_id"):
                st.rerun()

        # Age (Years & Months)
        col_age1, col_age2 = st.columns(2)
        with col_age1:
            age_years = st.number_input("Age (Years)", min_value=18, max_value=80, value=35)
        with col_age2:
            age_months = st.selectbox("Months", list(range(12)), index=0)

        age_total_months = convert_age_to_months(age_years, age_months)

        income = st.number_input("Annual Income (₹)", min_value=200000.0, value=750000.0, step=50000.0)

        # Employment Type with subcategories
        employment_main = st.selectbox("Employment Type", ["Employed", "Self-employed", "Business Owner", "Retired"])

        employment_type = employment_main
        if employment_main == "Self-employed":
            employment_sub = st.selectbox("Self-employed Category", ["Agriculture", "Business"])
            employment_type = f"Self-employed ({employment_sub})"

    with col2:
        st.markdown("#### 💰 Loan Details & Liabilities")
        credit_score = st.slider("Credit Score", min_value=300, max_value=850, value=720)
        loan_amount = st.number_input("Loan Amount (₹)", min_value=100000.0, value=2500000.0, step=100000.0)

        # Tenure (Predefined Options)
        tenure_options = [5, 10, 15, 20, 25, 30, "Random"]
        tenure_selected = st.selectbox("Tenure (Years)", tenure_options, index=5)

        if tenure_selected == "Random":
            tenure_years = random.choice([5, 10, 15, 20, 25, 30])
        else:
            tenure_years = tenure_selected

        tenure_months = tenure_years * 12

        st.markdown("**Existing Liabilities:**")

        # Liability breakdown
        col_liab1, col_liab2 = st.columns(2)
        with col_liab1:
            land_value = st.number_input("Land Value (₹)", min_value=0.0, value=0.0, step=100000.0, key="land")
        with col_liab2:
            car_value = st.number_input("Car Value (₹)", min_value=0.0, value=0.0, step=50000.0, key="car")

        other_value = st.number_input("Other Liabilities (₹)", min_value=0.0, value=0.0, step=50000.0, key="other")

        existing_liabilities = land_value + car_value + other_value

        # Display total
        st.metric("Total Liabilities", f"${existing_liabilities:,.2f}")

    st.markdown("#### 📍 Location")
    location = st.selectbox("Location", ["India"], index=0)

    st.markdown("</div>", unsafe_allow_html=True)

    # Styled button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        analyze_button = st.button("🚀 ANALYZE APPLICATION", use_container_width=True, key="analyze_btn")

    if analyze_button:
        with st.spinner("🔄 Analyzing application..."):
            try:
                payload = {
                    "applicant_id": applicant_id,
                    "age": age_total_months // 12,
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

                    # Determine styling - Light Green for Success, Blood Red for Failure
                    decision = result["decision"]
                    if decision == "Approved":
                        box_class = "approved-box"
                        status_class = "status-approved"
                        decision_icon = "✅"
                    elif decision == "Rejected":
                        box_class = "rejected-box"
                        status_class = "status-rejected"
                        decision_icon = "❌"
                    else:
                        box_class = "review-box"
                        status_class = "status-review"
                        decision_icon = "⚠️"

                    # Display Application Profile
                    st.markdown("<div class='section-header'>📋 Application Profile</div>", unsafe_allow_html=True)
                    col_prof1, col_prof2 = st.columns(2)

                    with col_prof1:
                        st.write(f"**Applicant ID:** {applicant_id}")
                        st.write(f"**Age:** {age_years} years {age_months} months")
                        st.write(f"**Employment:** {employment_type}")
                        st.write(f"**Credit Score:** {credit_score}")

                    with col_prof2:
                        st.write(f"**Loan Amount:** ₹{loan_amount:,.0f}")
                        st.write(f"**Tenure:** {tenure_years} years")
                        st.write(f"**Location:** {location}")
                        if existing_liabilities > 0:
                            st.write(f"**Liabilities:** ₹{existing_liabilities:,.0f}")
                            if land_value > 0:
                                st.write(f"  └─ Land: ₹{land_value:,.0f}")
                            if car_value > 0:
                                st.write(f"  └─ Car: ₹{car_value:,.0f}")
                            if other_value > 0:
                                st.write(f"  └─ Other: ₹{other_value:,.0f}")

                    st.divider()

                    st.markdown(f"""
                    <div class='result-box {box_class}'>
                        <h2 style='margin-top: 0; text-align: center;'>{decision_icon} <span class='{status_class}'>{decision}</span></h2>
                        <hr style='border: 2px solid currentColor;'>
                        <table style='width: 100%;'>
                            <tr><td><strong>📊 Risk Score:</strong></td><td>{result['risk_score']}/1000</td></tr>
                            <tr><td><strong>🎯 Confidence Level:</strong></td><td>{result['confidence_level']}</td></tr>
                            <tr><td><strong>🆔 Case ID:</strong></td><td>{result['case_id']}</td></tr>
                            <tr><td><strong>⏰ Timestamp:</strong></td><td>{result['timestamp']}</td></tr>
                            <tr><td colspan='2'><strong>📝 Analysis:</strong></td></tr>
                            <tr><td colspan='2'>{result['explanation']}</td></tr>
                        </table>
                    </div>
                    """, unsafe_allow_html=True)

                    # Display Analysis Graphs
                    st.markdown("<div class='section-header'>📊 Financial Analysis</div>", unsafe_allow_html=True)

                    import matplotlib.pyplot as plt
                    import numpy as np

                    col_graph1, col_graph2 = st.columns(2)

                    # Graph 1: Financial Breakdown
                    with col_graph1:
                        st.markdown("**💰 Financial Breakdown**")
                        fig, ax = plt.subplots(figsize=(8, 6))

                        categories = ["Annual Income", "Loan Amount", "Liabilities"]
                        values = [income, loan_amount, existing_liabilities]
                        colors = ["#2d5016", "#003366", "#8B0000"]

                        bars = ax.bar(categories, values, color=colors, edgecolor="black", linewidth=2)

                        # Add value labels on bars
                        for bar, value in zip(bars, values):
                            height = bar.get_height()
                            ax.text(
                                bar.get_x() + bar.get_width()/2.,
                                height,
                                f"₹{value:,.0f}",
                                ha="center",
                                va="bottom",
                                fontsize=10,
                                fontweight="bold"
                            )

                        ax.set_ylabel("Amount (₹)", fontweight="bold")
                        ax.set_title("Financial Profile", fontweight="bold", fontsize=12)
                        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"₹{x/100000:.0f}L"))
                        plt.xticks(rotation=15)
                        plt.tight_layout()
                        st.pyplot(fig)

                    # Graph 2: Risk Score Gauge
                    with col_graph2:
                        st.markdown("**📈 Risk Assessment**")
                        fig, ax = plt.subplots(figsize=(8, 6))

                        risk_score = result['risk_score']
                        risk_percentage = (risk_score / 1000) * 100

                        # Color based on risk
                        if risk_score < 300:
                            color = "#2d5016"  # Green - Low Risk
                            status = "Low Risk"
                        elif risk_score < 600:
                            color = "#ff8c00"  # Orange - Medium Risk
                            status = "Medium Risk"
                        else:
                            color = "#8B0000"  # Red - High Risk
                            status = "High Risk"

                        # Create gauge-like bar
                        ax.barh(0, risk_percentage, color=color, height=0.5, edgecolor="black", linewidth=2)
                        ax.set_xlim(0, 100)
                        ax.set_ylim(-1, 1)
                        ax.set_xlabel("Risk Percentage (%)", fontweight="bold")
                        ax.set_title(f"Risk Score: {risk_score}/1000 - {status}", fontweight="bold", fontsize=12)
                        ax.set_yticks([])
                        ax.grid(axis="x", alpha=0.3)

                        # Add percentage text
                        ax.text(risk_percentage/2, 0, f"{risk_percentage:.1f}%",
                               va="center", ha="center", fontsize=12, fontweight="bold", color="white")

                        plt.tight_layout()
                        st.pyplot(fig)

                    # Graph 3: DTI and Affordability Analysis
                    st.markdown("**📊 Loan Affordability Analysis**")
                    col_graph3, col_graph4 = st.columns(2)

                    with col_graph3:
                        # DTI Ratio Breakdown
                        fig, ax = plt.subplots(figsize=(8, 6))

                        monthly_income = income / 12
                        monthly_payment = loan_amount / (tenure_years * 12)
                        total_monthly_debt = monthly_payment + (existing_liabilities / 12)
                        dti_ratio = (total_monthly_debt / monthly_income) * 100 if monthly_income > 0 else 0

                        categories = ["Monthly Income", "Loan Payment", "Liability Payment"]
                        values = [monthly_income, monthly_payment, existing_liabilities / 12]
                        colors = ["#2d5016", "#003366", "#ff6b6b"]

                        bars = ax.bar(categories, values, color=colors, edgecolor="black", linewidth=2)

                        for bar, value in zip(bars, values):
                            height = bar.get_height()
                            ax.text(
                                bar.get_x() + bar.get_width()/2.,
                                height,
                                f"₹{value:,.0f}",
                                ha="center",
                                va="bottom",
                                fontsize=9,
                                fontweight="bold"
                            )

                        ax.set_ylabel("Monthly Amount (₹)", fontweight="bold")
                        ax.set_title("Monthly Payment Analysis", fontweight="bold", fontsize=12)
                        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"₹{x/1000:.0f}K"))
                        plt.xticks(rotation=15)
                        plt.tight_layout()
                        st.pyplot(fig)

                    with col_graph4:
                        # Loan vs Income Ratio
                        fig, ax = plt.subplots(figsize=(8, 6))

                        loan_to_income = (loan_amount / income) * 100

                        data = [loan_to_income, 100 - loan_to_income]
                        labels = [f"Loan Amount\n{loan_to_income:.1f}%", f"Other Income\n{100-loan_to_income:.1f}%"]
                        colors = ["#003366", "#e8f5e9"]
                        explode = (0.05, 0)

                        wedges, texts, autotexts = ax.pie(data, labels=labels, colors=colors, autopct="%1.1f%%",
                                                          startangle=90, explode=explode, textprops={"fontsize": 10, "fontweight": "bold"},
                                                          wedgeprops={"edgecolor": "black", "linewidth": 2})

                        ax.set_title("Loan-to-Income Ratio", fontweight="bold", fontsize=12)
                        plt.tight_layout()
                        st.pyplot(fig)

                    # Store result in session
                    if 'results' not in st.session_state:
                        st.session_state.results = []
                    st.session_state.results.append(result)

                else:
                    st.error(f"❌ API Error: {response.status_code} - {response.text}")

            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to API. Make sure FastAPI service is running on http://localhost:8000")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

with tab2:
    st.markdown("<div class='section-header'>📦 Batch Processing</div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background-color: #f0f4f8; padding: 15px; border-radius: 8px; border-left: 4px solid #003366; margin-bottom: 20px;'>
    📤 Upload a JSON file with multiple loan applications for AI-powered batch analysis and approval.
    </div>
    """, unsafe_allow_html=True)

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
    st.markdown("<div class='section-header'>📊 Decision Analytics & History</div>", unsafe_allow_html=True)

    # Get statistics from database
    stats = get_statistics()

    # Summary metrics from database with TD Bank styling
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class='metric-card' style='text-align: center;'>
        <div style='font-size: 2em; font-weight: bold; color: #003366;'>""" + str(stats['total_processed']) + """</div>
        <div style='color: #666;'>Total Processed</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class='metric-card' style='text-align: center; background-color: #e8f5e9; border-color: #2d5016;'>
        <div style='font-size: 2em; font-weight: bold; color: #2d5016;'>✅ {stats['approved']}</div>
        <div style='color: #2d5016;'>Approved</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class='metric-card' style='text-align: center; background-color: #ffebee; border-color: #8B0000;'>
        <div style='font-size: 2em; font-weight: bold; color: #8B0000;'>❌ {stats['rejected']}</div>
        <div style='color: #8B0000;'>Rejected</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class='metric-card' style='text-align: center; background-color: #fff8e1; border-color: #ff8c00;'>
        <div style='font-size: 2em; font-weight: bold; color: #ff8c00;'>⚠️ {stats['manual_review']}</div>
        <div style='color: #ff8c00;'>Review</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Average risk score
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Average Risk Score", f"{stats['average_risk_score']}/1000")
    with col2:
        approval_rate = (stats['approved'] / stats['total_processed'] * 100) if stats['total_processed'] > 0 else 0
        st.metric("Approval Rate", f"{approval_rate:.1f}%")

    st.divider()

    # Risk score distribution from database
    st.subheader("📈 Risk Score Distribution (0-1000 Scale)")
    risk_scores = get_risk_scores()
    if risk_scores:
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(risk_scores, bins=10, color='steelblue', edgecolor='black', linewidth=1.5)
        ax.set_xlabel("Risk Score (0-1000)", fontweight="bold")
        ax.set_ylabel("Frequency", fontweight="bold")
        ax.set_title("Distribution of Risk Scores (All Time)", fontweight="bold")
        ax.grid(axis="y", alpha=0.3)
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
<div class='footer-watermark'>
    <p style='font-size: 1.1em;'><strong>🏦 TD BANK - Intelligent Loan Approval System</strong></p>
    <p>Powered by Claude AI & LangGraph | User: Anupam</p>
    <p style='color: #999; font-size: 0.85em;'>✅ <span style='color: #2d5016;'>Light Green: Approved</span> | ❌ <span style='color: #8B0000;'>Blood Red: Rejected</span> | ⚠️ <span style='color: #ff8c00;'>Orange: Manual Review</span></p>
    <p style='color: #aaa; font-size: 0.8em;'>© 2024 TD Bank. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
