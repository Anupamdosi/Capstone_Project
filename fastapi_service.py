"""FastAPI microservice for loan application processing with LangGraph orchestration."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from typing import TypedDict
from langgraph.graph import StateGraph
from anthropic import Anthropic
from agents import (
    ApplicantData,
    ApplicantProfileAgent,
    FinancialRiskAgent,
    LoanDecisionAgent,
    ComplianceOrchestratorAgent
)
from database import init_database, save_application, get_statistics
from datetime import datetime

app = FastAPI(title="Loan Approval Microservice", version="1.0.0")

# Initialize database on startup
init_database()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LoanApplicationRequest(BaseModel):
    """Loan application request model."""
    applicant_id: str
    age: int
    income: float
    employment_type: str
    credit_score: int
    loan_amount: float
    tenure_months: int
    existing_liabilities: float
    location: str


class LoanApprovalResponse(BaseModel):
    """Loan approval response model."""
    decision: str
    risk_score: float
    confidence_level: str
    explanation: str
    case_id: str
    timestamp: str


# LangGraph State Definition
class LoanApplicationState(TypedDict):
    """State for loan application processing workflow."""
    applicant_data: ApplicantData
    applicant_profile: dict
    financial_risk: dict
    loan_decision: dict
    compliance_result: dict


# Claude API Client for LLM-powered explanations
claude_client = Anthropic()


def generate_llm_explanation(decision: str, risk_score: float, applicant_data: dict, financial_risk: dict) -> str:
    """Generate natural language explanation using Claude API."""
    try:
        prompt = f"""
        You are a loan officer at TD Bank. Provide a professional, concise explanation for this loan decision.

        Decision: {decision}
        Risk Score: {risk_score}/1000

        Applicant Information:
        - Age: {applicant_data.get('age')} years
        - Income: ₹{applicant_data.get('income'):,.0f}
        - Employment: {applicant_data.get('employment_type')}
        - Credit Score: {applicant_data.get('credit_score')}/850
        - Loan Amount: ₹{applicant_data.get('loan_amount'):,.0f}
        - Tenure: {applicant_data.get('tenure_months') // 12} years
        - Existing Liabilities: ₹{applicant_data.get('existing_liabilities'):,.0f}
        - Location: {applicant_data.get('location')}

        Financial Analysis:
        - Debt-to-Income Ratio: {financial_risk.get('debt_to_income_ratio'):.2%}
        - Credit Risk: {financial_risk.get('credit_score_risk_level')}
        - Loan Amount Risk: {financial_risk.get('loan_amount_risk')}

        Provide a 2-3 sentence explanation suitable for customer communication. Be professional, clear, and empathetic.
        """

        response = claude_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.content[0].text
    except Exception as e:
        print(f"Claude API error: {e}")
        # Fallback to rule-based explanation if Claude API fails
        if decision == "Approved":
            return f"Application approved. Risk score: {risk_score:.0f}/1000. Strong financial profile."
        elif decision == "Requires Manual Review":
            return f"Manual review required. Risk score: {risk_score:.0f}/1000. Additional verification needed."
        else:
            return f"Application rejected. Risk score: {risk_score:.0f}/1000. Financial risk exceeds acceptable threshold."


# LangGraph Node Functions
def applicant_profile_node(state: LoanApplicationState) -> LoanApplicationState:
    """Analyze applicant profile."""
    state["applicant_profile"] = ApplicantProfileAgent.analyze(state["applicant_data"])
    return state


def financial_risk_node(state: LoanApplicationState) -> LoanApplicationState:
    """Analyze financial risk."""
    state["financial_risk"] = FinancialRiskAgent.analyze(state["applicant_data"])
    return state


def loan_decision_node(state: LoanApplicationState) -> LoanApplicationState:
    """Make loan decision."""
    state["loan_decision"] = LoanDecisionAgent.decide(
        state["applicant_profile"],
        state["financial_risk"]
    )
    return state


def compliance_node(state: LoanApplicationState) -> LoanApplicationState:
    """Process compliance and generate notification."""
    state["compliance_result"] = ComplianceOrchestratorAgent.process(state["loan_decision"])
    return state


# Create and compile LangGraph workflow
def create_loan_workflow():
    """Create and compile the loan approval workflow using LangGraph."""
    workflow = StateGraph(LoanApplicationState)

    # Add nodes
    workflow.add_node("applicant_profile", applicant_profile_node)
    workflow.add_node("financial_risk", financial_risk_node)
    workflow.add_node("loan_decision", loan_decision_node)
    workflow.add_node("compliance", compliance_node)

    # Add edges (workflow steps)
    workflow.add_edge("applicant_profile", "financial_risk")
    workflow.add_edge("financial_risk", "loan_decision")
    workflow.add_edge("loan_decision", "compliance")

    # Set entry and exit points
    workflow.set_entry_point("applicant_profile")
    workflow.set_finish_point("compliance")

    return workflow.compile()


# Compile the workflow
loan_workflow = create_loan_workflow()


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/analyze_loan_application", response_model=LoanApprovalResponse)
async def analyze_loan_application(request: LoanApplicationRequest):
    """
    Analyze loan application using LangGraph-orchestrated multi-agent system.

    Workflow:
    1. Initialize loan application state
    2. Run LangGraph workflow orchestrating agents
    3. Generate Claude-powered explanation
    4. Persist results to database
    5. Return response
    """
    try:
        # Create applicant data object
        applicant_data = ApplicantData(
            applicant_id=request.applicant_id,
            age=request.age,
            income=request.income,
            employment_type=request.employment_type,
            credit_score=request.credit_score,
            loan_amount=request.loan_amount,
            tenure_months=request.tenure_months,
            existing_liabilities=request.existing_liabilities,
            location=request.location
        )

        # Initialize state for LangGraph workflow
        initial_state: LoanApplicationState = {
            "applicant_data": applicant_data,
            "applicant_profile": {},
            "financial_risk": {},
            "loan_decision": {},
            "compliance_result": {}
        }

        # Execute LangGraph workflow
        final_state = loan_workflow.invoke(initial_state)

        # Extract results from workflow state
        loan_decision = final_state["loan_decision"]
        compliance_result = final_state["compliance_result"]

        # Generate Claude-powered explanation
        llm_explanation = generate_llm_explanation(
            loan_decision["decision"],
            loan_decision["risk_score"],
            {
                "age": request.age,
                "income": request.income,
                "employment_type": request.employment_type,
                "credit_score": request.credit_score,
                "loan_amount": request.loan_amount,
                "tenure_months": request.tenure_months,
                "existing_liabilities": request.existing_liabilities,
                "location": request.location
            },
            final_state["financial_risk"]
        )

        # Prepare response
        response = LoanApprovalResponse(
            decision=loan_decision["decision"],
            risk_score=loan_decision["risk_score"],
            confidence_level=loan_decision["confidence_level"],
            explanation=llm_explanation,  # Use Claude-generated explanation
            case_id=compliance_result["case_id"],
            timestamp=compliance_result["timestamp"]
        )

        # Save to database
        save_application(
            {
                "applicant_id": request.applicant_id,
                "age": request.age,
                "income": request.income,
                "employment_type": request.employment_type,
                "credit_score": request.credit_score,
                "loan_amount": request.loan_amount,
                "tenure_months": request.tenure_months,
                "existing_liabilities": request.existing_liabilities,
                "location": request.location
            },
            {
                "decision": response.decision,
                "risk_score": response.risk_score,
                "confidence_level": response.confidence_level,
                "explanation": response.explanation,
                "case_id": response.case_id,
                "timestamp": response.timestamp
            }
        )

        return response

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/batch_analyze")
async def batch_analyze(requests_list: list[LoanApplicationRequest]):
    """Batch process multiple loan applications."""
    results = []
    for request in requests_list:
        try:
            result = await analyze_loan_application(request)
            results.append({"status": "success", "data": result})
        except Exception as e:
            results.append({"status": "error", "applicant_id": request.applicant_id, "error": str(e)})
    return results


@app.get("/statistics")
async def get_stats():
    """Get summary statistics of all processed applications."""
    stats = get_statistics()
    return stats


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
