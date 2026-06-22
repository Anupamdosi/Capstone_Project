"""Domain-specific agents for loan approval system."""

from typing import TypedDict
from dataclasses import dataclass
import json


@dataclass
class ApplicantData:
    """Loan application data."""
    applicant_id: str
    age: int
    income: float
    employment_type: str
    credit_score: int
    loan_amount: float
    tenure_months: int
    existing_liabilities: float
    location: str


class ApplicantProfileAgent:
    """Analyzes applicant profile for income stability and employment risk."""

    @staticmethod
    def analyze(data: ApplicantData) -> dict:
        """Analyze applicant profile."""
        income_stability = ApplicantProfileAgent._calculate_income_stability(
            data.income, data.employment_type
        )
        employment_risk = ApplicantProfileAgent._calculate_employment_risk(
            data.employment_type, data.age
        )

        return {
            "income_stability_score": income_stability,
            "employment_risk": employment_risk,
            "credit_history_summary": f"Credit Score: {data.credit_score}/850",
            "application_completeness": "Complete",
            "applicant_id": data.applicant_id
        }

    @staticmethod
    def _calculate_income_stability(income: float, employment_type: str) -> float:
        """Calculate income stability score (0-100)."""
        base_score = 60
        if employment_type == "Employed":
            base_score += 30
        elif employment_type == "Self-employed":
            base_score += 15
        elif employment_type == "Business Owner":
            base_score += 20
        return min(100, base_score)

    @staticmethod
    def _calculate_employment_risk(employment_type: str, age: int) -> str:
        """Calculate employment risk level."""
        if employment_type == "Employed" and age < 65:
            return "Low"
        elif employment_type == "Self-employed":
            return "Medium"
        elif employment_type == "Business Owner":
            return "Medium"
        else:
            return "High"


class FinancialRiskAgent:
    """Analyzes financial risk indicators."""

    @staticmethod
    def analyze(data: ApplicantData) -> dict:
        """Analyze financial risk."""
        dti = FinancialRiskAgent._calculate_dti(
            data.loan_amount, data.tenure_months, data.income, data.existing_liabilities
        )
        credit_risk = FinancialRiskAgent._calculate_credit_risk(data.credit_score)
        loan_risk = FinancialRiskAgent._calculate_loan_amount_risk(
            data.loan_amount, data.income
        )

        return {
            "debt_to_income_ratio": round(dti, 2),
            "credit_score_risk_level": credit_risk,
            "loan_amount_risk": loan_risk,
            "anomaly_detected": dti > 0.5,
            "reasoning": f"DTI: {dti:.2%}, Credit Risk: {credit_risk}, Loan Risk: {loan_risk}",
            "applicant_id": data.applicant_id
        }

    @staticmethod
    def _calculate_dti(loan_amount: float, tenure: int, income: float, liabilities: float) -> float:
        """Calculate debt-to-income ratio."""
        monthly_income = income / 12
        monthly_payment = (loan_amount / tenure)
        total_debt = monthly_payment + (liabilities / 12)
        if monthly_income == 0:
            return 1.0
        return total_debt / monthly_income

    @staticmethod
    def _calculate_credit_risk(credit_score: int) -> str:
        """Determine credit risk level."""
        if credit_score >= 750:
            return "Low"
        elif credit_score >= 650:
            return "Medium"
        else:
            return "High"

    @staticmethod
    def _calculate_loan_amount_risk(loan_amount: float, income: float) -> str:
        """Determine loan amount risk."""
        loan_to_income = loan_amount / income
        if loan_to_income < 3:
            return "Low"
        elif loan_to_income < 5:
            return "Medium"
        else:
            return "High"


class LoanDecisionAgent:
    """Makes the final loan approval decision."""

    @staticmethod
    def decide(applicant_profile: dict, financial_risk: dict) -> dict:
        """Make loan decision based on analysis."""
        risk_score = LoanDecisionAgent._calculate_risk_score(
            applicant_profile, financial_risk
        )
        decision, confidence = LoanDecisionAgent._make_decision(risk_score, financial_risk)

        return {
            "decision": decision,
            "risk_score": round(risk_score, 2),
            "confidence_level": confidence,
            "key_factors": {
                "income_stability": applicant_profile["income_stability_score"],
                "dti_ratio": financial_risk["debt_to_income_ratio"],
                "credit_risk": financial_risk["credit_score_risk_level"],
                "employment_risk": applicant_profile["employment_risk"]
            },
            "explanation": LoanDecisionAgent._generate_explanation(
                decision, risk_score, financial_risk
            ),
            "applicant_id": applicant_profile["applicant_id"]
        }

    @staticmethod
    def _calculate_risk_score(applicant_profile: dict, financial_risk: dict) -> float:
        """Calculate overall risk score (0-100, higher = riskier)."""
        score = 50

        income_stability = applicant_profile["income_stability_score"]
        score -= (income_stability - 50) * 0.2

        if financial_risk["credit_score_risk_level"] == "Low":
            score -= 15
        elif financial_risk["credit_score_risk_level"] == "Medium":
            score += 5
        else:
            score += 20

        dti = financial_risk["debt_to_income_ratio"]
        if dti < 0.3:
            score -= 10
        elif dti > 0.5:
            score += 15

        if financial_risk["loan_amount_risk"] == "High":
            score += 10

        return max(0, min(100, score))

    @staticmethod
    def _make_decision(risk_score: float, financial_risk: dict) -> tuple:
        """Make approval decision based on risk score."""
        if risk_score < 30:
            return "Approved", "High"
        elif risk_score < 60:
            return "Requires Manual Review", "Medium"
        else:
            return "Rejected", "High"

    @staticmethod
    def _generate_explanation(decision: str, risk_score: float, financial_risk: dict) -> str:
        """Generate explanation for the decision."""
        if decision == "Approved":
            return f"Application approved. Risk score: {risk_score:.1f}/100. Strong financial profile."
        elif decision == "Requires Manual Review":
            reason = f"DTI ratio is {financial_risk['debt_to_income_ratio']:.2%}" if financial_risk["debt_to_income_ratio"] > 0.4 else "Additional verification needed"
            return f"Manual review required. Risk score: {risk_score:.1f}/100. Reason: {reason}"
        else:
            return f"Application rejected. Risk score: {risk_score:.1f}/100. Financial risk exceeds acceptable threshold."


class ComplianceOrchestratorAgent:
    """Handles compliance and notification."""

    @staticmethod
    def process(loan_decision: dict) -> dict:
        """Process compliance and generate notification."""
        from datetime import datetime

        case_id = f"CASE-{loan_decision['applicant_id']}-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        return {
            "action_taken": loan_decision["decision"],
            "notification_sent": True,
            "case_id": case_id,
            "timestamp": datetime.now().isoformat(),
            "summary": f"Loan application {loan_decision['decision'].lower()}: {loan_decision['explanation']}",
            "applicant_id": loan_decision["applicant_id"]
        }
