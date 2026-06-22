"""FastAPI microservice for loan application processing."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from agents import (
    ApplicantData,
    ApplicantProfileAgent,
    FinancialRiskAgent,
    LoanDecisionAgent,
    ComplianceOrchestratorAgent
)
from database import init_database, save_application, get_statistics

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


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/analyze_loan_application", response_model=LoanApprovalResponse)
async def analyze_loan_application(request: LoanApplicationRequest):
    """
    Analyze loan application using multi-agent system.

    Flow:
    1. Create applicant data
    2. Run applicant profile analysis
    3. Run financial risk analysis
    4. Make loan decision
    5. Process compliance
    6. Return result
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

        # Run agent analyses
        applicant_profile = ApplicantProfileAgent.analyze(applicant_data)
        financial_risk = FinancialRiskAgent.analyze(applicant_data)
        loan_decision = LoanDecisionAgent.decide(applicant_profile, financial_risk)
        compliance_result = ComplianceOrchestratorAgent.process(loan_decision)

        # Prepare response
        response = LoanApprovalResponse(
            decision=loan_decision["decision"],
            risk_score=loan_decision["risk_score"],
            confidence_level=loan_decision["confidence_level"],
            explanation=loan_decision["explanation"],
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
