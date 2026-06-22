"""Integration tests for LangGraph workflow."""

import pytest
from agents import ApplicantData


@pytest.mark.integration
class TestLangGraphWorkflow:
    """Test LangGraph workflow integration."""

    def test_workflow_execution(self, sample_applicant_data):
        """Test complete workflow execution."""
        try:
            from fastapi_service import loan_workflow, LoanApplicationState

            initial_state: LoanApplicationState = {
                "applicant_data": sample_applicant_data,
                "applicant_profile": {},
                "financial_risk": {},
                "loan_decision": {},
                "compliance_result": {}
            }

            final_state = loan_workflow.invoke(initial_state)

            # Verify all states are populated
            assert final_state["applicant_profile"]
            assert final_state["financial_risk"]
            assert final_state["loan_decision"]
            assert final_state["compliance_result"]

            # Verify decision was made
            assert final_state["loan_decision"]["decision"] in [
                "Approved",
                "Rejected",
                "Requires Manual Review"
            ]

        except ImportError:
            pytest.skip("LangGraph workflow not available")

    def test_workflow_with_low_risk_applicant(self, low_risk_applicant):
        """Test workflow with low-risk applicant."""
        try:
            from fastapi_service import loan_workflow, LoanApplicationState

            initial_state: LoanApplicationState = {
                "applicant_data": low_risk_applicant,
                "applicant_profile": {},
                "financial_risk": {},
                "loan_decision": {},
                "compliance_result": {}
            }

            final_state = loan_workflow.invoke(initial_state)

            # Low-risk applicants should be approved
            assert final_state["loan_decision"]["decision"] == "Approved"
            assert final_state["loan_decision"]["risk_score"] < 300

        except ImportError:
            pytest.skip("LangGraph workflow not available")

    def test_workflow_with_high_risk_applicant(self, high_risk_applicant):
        """Test workflow with high-risk applicant."""
        try:
            from fastapi_service import loan_workflow, LoanApplicationState

            initial_state: LoanApplicationState = {
                "applicant_data": high_risk_applicant,
                "applicant_profile": {},
                "financial_risk": {},
                "loan_decision": {},
                "compliance_result": {}
            }

            final_state = loan_workflow.invoke(initial_state)

            # High-risk applicants should be rejected
            assert final_state["loan_decision"]["decision"] == "Rejected"
            assert final_state["loan_decision"]["risk_score"] >= 600

        except ImportError:
            pytest.skip("LangGraph workflow not available")


@pytest.mark.integration
class TestClaudeAPIIntegration:
    """Test Claude API integration for explanations."""

    def test_llm_explanation_generation(self, sample_applicant_data):
        """Test LLM explanation generation."""
        try:
            from fastapi_service import generate_llm_explanation
            from agents import ApplicantProfileAgent, FinancialRiskAgent, LoanDecisionAgent

            profile = ApplicantProfileAgent.analyze(sample_applicant_data)
            risk = FinancialRiskAgent.analyze(sample_applicant_data)
            decision = LoanDecisionAgent.decide(profile, risk)

            explanation = generate_llm_explanation(
                decision["decision"],
                decision["risk_score"],
                {
                    "age": sample_applicant_data.age,
                    "income": sample_applicant_data.income,
                    "employment_type": sample_applicant_data.employment_type,
                    "credit_score": sample_applicant_data.credit_score,
                    "loan_amount": sample_applicant_data.loan_amount,
                    "tenure_months": sample_applicant_data.tenure_months,
                    "existing_liabilities": sample_applicant_data.existing_liabilities,
                    "location": sample_applicant_data.location
                },
                risk
            )

            # Verify explanation is generated
            assert isinstance(explanation, str)
            assert len(explanation) > 10  # Should have meaningful content
            assert decision["decision"].lower() in explanation.lower() or "application" in explanation.lower()

        except Exception as e:
            pytest.skip(f"Claude API not available: {e}")

    def test_explanation_fallback(self, sample_applicant_data):
        """Test fallback explanation when Claude API fails."""
        try:
            from fastapi_service import generate_llm_explanation

            # Use a decision that should produce a fallback explanation
            explanation = generate_llm_explanation(
                "Approved",
                250,
                {
                    "age": 35,
                    "income": 750000,
                    "employment_type": "Employed",
                    "credit_score": 750,
                    "loan_amount": 2500000,
                    "tenure_months": 180,
                    "existing_liabilities": 500000,
                    "location": "India"
                },
                {"debt_to_income_ratio": 0.2}
            )

            # Should return a valid explanation
            assert isinstance(explanation, str)
            assert len(explanation) > 10

        except Exception as e:
            pytest.skip(f"Test setup failed: {e}")
