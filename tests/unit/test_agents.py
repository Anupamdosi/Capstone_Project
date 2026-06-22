"""Unit tests for agents module."""

import pytest
from agents import (
    ApplicantProfileAgent,
    FinancialRiskAgent,
    LoanDecisionAgent,
    ComplianceOrchestratorAgent,
    ApplicantData
)


class TestApplicantProfileAgent:
    """Test ApplicantProfileAgent."""

    def test_employed_profile(self, sample_applicant_data):
        """Test income stability for employed applicant."""
        result = ApplicantProfileAgent.analyze(sample_applicant_data)

        assert "income_stability_score" in result
        assert "employment_risk" in result
        assert result["employment_risk"] == "Low"  # Employed age < 65

    def test_self_employed_profile(self, sample_applicant_data):
        """Test income stability for self-employed applicant."""
        applicant = ApplicantData(
            applicant_id="TEST-001",
            age=35,
            income=500000.0,
            employment_type="Self-employed",
            credit_score=700,
            loan_amount=1000000.0,
            tenure_months=120,
            existing_liabilities=300000.0,
            location="India"
        )

        result = ApplicantProfileAgent.analyze(applicant)

        assert result["employment_risk"] == "Medium"
        assert result["income_stability_score"] == 75  # 60 + 15

    def test_business_owner_profile(self):
        """Test income stability for business owner."""
        applicant = ApplicantData(
            applicant_id="TEST-002",
            age=50,
            income=1000000.0,
            employment_type="Business Owner",
            credit_score=750,
            loan_amount=2000000.0,
            tenure_months=180,
            existing_liabilities=500000.0,
            location="India"
        )

        result = ApplicantProfileAgent.analyze(applicant)

        assert result["employment_risk"] == "Medium"
        assert result["income_stability_score"] == 80  # 60 + 20

    def test_profile_completeness(self, sample_applicant_data):
        """Test application completeness flag."""
        result = ApplicantProfileAgent.analyze(sample_applicant_data)

        assert result["application_completeness"] == "Complete"


class TestFinancialRiskAgent:
    """Test FinancialRiskAgent."""

    def test_dti_calculation_low_risk(self, low_risk_applicant):
        """Test DTI calculation for low-risk applicant."""
        result = FinancialRiskAgent.analyze(low_risk_applicant)

        dti = result["debt_to_income_ratio"]
        # Monthly income: 1500000 / 12 = 125000
        # Monthly payment: 1000000 / 240 = 4166.67
        # Monthly liabilities: 100000 / 12 = 8333.33
        # Total debt: 4166.67 + 8333.33 = 12500
        # DTI: 12500 / 125000 = 0.10

        assert 0.09 < dti < 0.11
        assert result["debt_to_income_ratio"] < 0.3

    def test_dti_calculation_high_risk(self, high_risk_applicant):
        """Test DTI calculation for high-risk applicant."""
        result = FinancialRiskAgent.analyze(high_risk_applicant)

        assert result["debt_to_income_ratio"] > 0.5
        assert result["anomaly_detected"] is True

    def test_credit_risk_levels(self):
        """Test credit risk categorization."""
        # High credit score
        low_risk = ApplicantData(
            applicant_id="TEST-003",
            age=40,
            income=1000000.0,
            employment_type="Employed",
            credit_score=800,
            loan_amount=1000000.0,
            tenure_months=120,
            existing_liabilities=0.0,
            location="India"
        )
        result = FinancialRiskAgent.analyze(low_risk)
        assert result["credit_score_risk_level"] == "Low"

        # Medium credit score
        med_risk = ApplicantData(
            applicant_id="TEST-004",
            age=40,
            income=1000000.0,
            employment_type="Employed",
            credit_score=700,
            loan_amount=1000000.0,
            tenure_months=120,
            existing_liabilities=0.0,
            location="India"
        )
        result = FinancialRiskAgent.analyze(med_risk)
        assert result["credit_score_risk_level"] == "Medium"

        # Low credit score
        high_risk = ApplicantData(
            applicant_id="TEST-005",
            age=40,
            income=1000000.0,
            employment_type="Employed",
            credit_score=600,
            loan_amount=1000000.0,
            tenure_months=120,
            existing_liabilities=0.0,
            location="India"
        )
        result = FinancialRiskAgent.analyze(high_risk)
        assert result["credit_score_risk_level"] == "High"

    def test_loan_to_income_ratio(self):
        """Test loan amount risk categorization."""
        # Low LTI
        low_lti = ApplicantData(
            applicant_id="TEST-006",
            age=40,
            income=1000000.0,
            employment_type="Employed",
            credit_score=700,
            loan_amount=1500000.0,  # 1.5x income
            tenure_months=120,
            existing_liabilities=0.0,
            location="India"
        )
        result = FinancialRiskAgent.analyze(low_lti)
        assert result["loan_amount_risk"] == "Low"

        # High LTI
        high_lti = ApplicantData(
            applicant_id="TEST-007",
            age=40,
            income=500000.0,
            employment_type="Employed",
            credit_score=700,
            loan_amount=3000000.0,  # 6x income
            tenure_months=120,
            existing_liabilities=0.0,
            location="India"
        )
        result = FinancialRiskAgent.analyze(high_lti)
        assert result["loan_amount_risk"] == "High"


class TestLoanDecisionAgent:
    """Test LoanDecisionAgent."""

    def test_risk_score_range(self, sample_applicant_data):
        """Test risk score is within valid range."""
        profile = ApplicantProfileAgent.analyze(sample_applicant_data)
        risk = FinancialRiskAgent.analyze(sample_applicant_data)

        decision = LoanDecisionAgent.decide(profile, risk)

        assert 0 <= decision["risk_score"] <= 1000

    def test_low_risk_approval(self, low_risk_applicant):
        """Test low-risk applicant gets approved."""
        profile = ApplicantProfileAgent.analyze(low_risk_applicant)
        risk = FinancialRiskAgent.analyze(low_risk_applicant)

        decision = LoanDecisionAgent.decide(profile, risk)

        assert decision["decision"] == "Approved"
        assert decision["risk_score"] < 300

    def test_high_risk_rejection(self, high_risk_applicant):
        """Test high-risk applicant gets rejected."""
        profile = ApplicantProfileAgent.analyze(high_risk_applicant)
        risk = FinancialRiskAgent.analyze(high_risk_applicant)

        decision = LoanDecisionAgent.decide(profile, risk)

        assert decision["decision"] == "Rejected"
        assert decision["risk_score"] >= 600

    def test_medium_risk_review(self, medium_risk_applicant):
        """Test medium-risk applicant gets manual review."""
        profile = ApplicantProfileAgent.analyze(medium_risk_applicant)
        risk = FinancialRiskAgent.analyze(medium_risk_applicant)

        decision = LoanDecisionAgent.decide(profile, risk)

        assert decision["decision"] == "Requires Manual Review"
        assert 300 <= decision["risk_score"] < 600

    def test_confidence_levels(self, sample_applicant_data):
        """Test confidence levels are assigned."""
        profile = ApplicantProfileAgent.analyze(sample_applicant_data)
        risk = FinancialRiskAgent.analyze(sample_applicant_data)

        decision = LoanDecisionAgent.decide(profile, risk)

        assert decision["confidence_level"] in ["Low", "Medium", "High"]
        assert "key_factors" in decision
        assert "explanation" in decision


class TestComplianceOrchestratorAgent:
    """Test ComplianceOrchestratorAgent."""

    def test_case_id_generation(self, sample_applicant_data):
        """Test case ID is generated properly."""
        profile = ApplicantProfileAgent.analyze(sample_applicant_data)
        risk = FinancialRiskAgent.analyze(sample_applicant_data)
        decision = LoanDecisionAgent.decide(profile, risk)

        result = ComplianceOrchestratorAgent.process(decision)

        assert "case_id" in result
        assert result["case_id"].startswith("CASE-")
        assert "APP-TEST-001" in result["case_id"]

    def test_notification_sent_flag(self, sample_applicant_data):
        """Test notification flag is set."""
        profile = ApplicantProfileAgent.analyze(sample_applicant_data)
        risk = FinancialRiskAgent.analyze(sample_applicant_data)
        decision = LoanDecisionAgent.decide(profile, risk)

        result = ComplianceOrchestratorAgent.process(decision)

        assert result["notification_sent"] is True

    def test_compliance_action(self, sample_applicant_data):
        """Test compliance action matches decision."""
        profile = ApplicantProfileAgent.analyze(sample_applicant_data)
        risk = FinancialRiskAgent.analyze(sample_applicant_data)
        decision = LoanDecisionAgent.decide(profile, risk)

        result = ComplianceOrchestratorAgent.process(decision)

        assert result["action_taken"] == decision["decision"]


@pytest.mark.unit
class TestRiskScoreCalculation:
    """Test risk score calculation logic."""

    def test_risk_score_improves_with_better_income(self):
        """Test risk score improves with higher income stability."""
        poor_income = ApplicantData(
            applicant_id="POOR",
            age=35,
            income=300000.0,
            employment_type="Self-employed",
            credit_score=700,
            loan_amount=1000000.0,
            tenure_months=120,
            existing_liabilities=500000.0,
            location="India"
        )

        good_income = ApplicantData(
            applicant_id="GOOD",
            age=35,
            income=1500000.0,
            employment_type="Employed",
            credit_score=700,
            loan_amount=1000000.0,
            tenure_months=120,
            existing_liabilities=500000.0,
            location="India"
        )

        profile1 = ApplicantProfileAgent.analyze(poor_income)
        risk1 = FinancialRiskAgent.analyze(poor_income)
        decision1 = LoanDecisionAgent.decide(profile1, risk1)

        profile2 = ApplicantProfileAgent.analyze(good_income)
        risk2 = FinancialRiskAgent.analyze(good_income)
        decision2 = LoanDecisionAgent.decide(profile2, risk2)

        # Good income should have lower risk score
        assert decision2["risk_score"] < decision1["risk_score"]
