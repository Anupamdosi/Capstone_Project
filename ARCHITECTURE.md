# Architecture Documentation

## System Overview

The Agentic AI Intelligent Loan Approval System is a distributed multi-agent architecture designed for scalable, explainable loan decision-making.

```
┌─────────────────────────────────────────────────────────┐
│              User Interface Layer                        │
│         Streamlit Web Application (Port 8501)           │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP
┌────────────────────▼────────────────────────────────────┐
│           Application Layer                             │
│      FastAPI REST Service (Port 8000)                  │
│  ┌──────────────────────────────────────────────────┐  │
│  │  POST /analyze_loan_application                  │  │
│  │  POST /batch_analyze                            │  │
│  │  GET  /health                                   │  │
│  └──────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│        Orchestration & Business Logic Layer             │
│              LangGraph Orchestrator                     │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Request Validation & Routing                    │  │
│  │ Agent Workflow Coordination                     │  │
│  │ State Management & Decision Synthesis           │  │
│  └──────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┬────────────┐
        │            │            │            │
┌───────▼────┐ ┌─────▼──────┐ ┌──▼──────────┐ ┌──▼──────────────┐
│ Applicant  │ │ Financial  │ │ Loan        │ │ Compliance &    │
│ Profile    │ │ Risk       │ │ Decision    │ │ Orchestrator    │
│ Agent      │ │ Agent      │ │ Agent       │ │ Agent           │
└────────────┘ └────────────┘ └─────────────┘ └─────────────────┘
```

## Layer Descriptions

### 1. User Interface Layer
**Technology**: Streamlit
**Responsibility**: Present UI, handle user interactions, display results
**Key Features**:
- Single application form with real-time validation
- Batch processing upload
- Interactive analytics dashboard
- Decision history and metrics

**Port**: 8501
**Access**: `http://localhost:8501`

### 2. Application Layer
**Technology**: FastAPI
**Responsibility**: HTTP request handling, input validation, response formatting
**Key Features**:
- RESTful API endpoints
- Pydantic model validation
- CORS middleware
- Error handling and logging

**Port**: 8000
**Endpoints**:
- `POST /analyze_loan_application` - Single application
- `POST /batch_analyze` - Multiple applications
- `GET /health` - Service health

**Request Validation**:
- All numeric fields validated (age, income, credit score, etc.)
- Employment type enum validation
- Tenure bounds checking
- Applicant ID uniqueness

### 3. Orchestration Layer
**Technology**: Python-based Orchestrator
**Responsibility**: Workflow management and state coordination
**Flow**:
1. Receive validated request
2. Create applicant data object
3. Invoke agents in sequence
4. Aggregate results
5. Return synthesized decision

**State Management**:
```python
{
  "applicant_data": {...},
  "applicant_profile": {...},
  "financial_risk": {...},
  "loan_decision": {...},
  "compliance_result": {...}
}
```

### 4. Agent Layer
**Technology**: Python-based Domain-Specific Agents
**Responsibility**: Specialized analysis and decision-making

## Detailed Agent Architecture

### Agent 1: Applicant Profile Agent
**Purpose**: Analyze applicant demographics and employment
**Inputs**:
- Age (18-80)
- Income (annual)
- Employment Type (Employed, Self-employed, Business Owner, Retired)
- Credit Score (300-850)

**Processing**:
```python
Income Stability Score = Base(60) + Employment Adjustment(-20 to +30)
Employment Risk = Function(Employment Type, Age)
```

**Outputs**:
```json
{
  "income_stability_score": 85,
  "employment_risk": "Low",
  "credit_history_summary": "Credit Score: 720/850",
  "application_completeness": "Complete",
  "applicant_id": "APP-001"
}
```

### Agent 2: Financial Risk Agent
**Purpose**: Analyze financial metrics and risk indicators
**Inputs**:
- Annual Income
- Loan Amount
- Tenure (months)
- Existing Liabilities

**Processing**:
```python
DTI = (Monthly Loan Payment + Monthly Liabilities) / Monthly Income
Credit Risk = Function(Credit Score)
Loan Amount Risk = Function(Loan Amount / Income)
```

**Risk Levels**:
- Credit Risk: Low (≥750), Medium (650-749), High (<650)
- Loan Risk: Low (<3x), Medium (3-5x), High (>5x)

**Outputs**:
```json
{
  "debt_to_income_ratio": 0.35,
  "credit_score_risk_level": "Low",
  "loan_amount_risk": "Low",
  "anomaly_detected": false,
  "reasoning": "DTI: 35.00%, Credit Risk: Low, Loan Risk: Low",
  "applicant_id": "APP-001"
}
```

### Agent 3: Loan Decision Agent
**Purpose**: Make final approval decision based on all analysis
**Inputs**:
- Applicant Profile (from Agent 1)
- Financial Risk Assessment (from Agent 2)

**Processing**:
```python
Risk Score (0-100):
  = Base(50)
  - Income Stability Impact(-20 to +20)
  ± Credit Risk Impact(-15 to +20)
  ± DTI Impact(-10 to +15)
  ± Loan Amount Risk Impact(0 to +10)

Decision Logic:
  Risk Score < 30      → Approved (High Confidence)
  Risk Score 30-60     → Manual Review (Medium Confidence)
  Risk Score > 60      → Rejected (High Confidence)
```

**Outputs**:
```json
{
  "decision": "Approved",
  "risk_score": 35.5,
  "confidence_level": "High",
  "key_factors": {
    "income_stability": 85,
    "dti_ratio": 0.35,
    "credit_risk": "Low",
    "employment_risk": "Low"
  },
  "explanation": "Application approved. Risk score: 35.5/100. Strong financial profile.",
  "applicant_id": "APP-001"
}
```

### Agent 4: Compliance & Action Orchestrator
**Purpose**: Generate compliance records and notifications
**Inputs**:
- Loan Decision (from Agent 3)

**Processing**:
```python
Case ID = "CASE-" + Applicant ID + Timestamp
Notification = Send to system
```

**Outputs**:
```json
{
  "action_taken": "Approved",
  "notification_sent": true,
  "case_id": "CASE-APP-001-20240619102030",
  "timestamp": "2024-06-19T10:20:30.123456",
  "summary": "Loan application approved: Application approved. Risk score: 35.5/100. Strong financial profile.",
  "applicant_id": "APP-001"
}
```

## Data Flow

### Single Application Flow
```
User Input (Streamlit)
    ↓
HTTP POST Request (FastAPI)
    ↓
Request Validation (Pydantic)
    ↓
Orchestrator
    ├→ Agent 1: Profile Analysis
    ├→ Agent 2: Financial Risk
    ├→ Agent 3: Decision Making
    └→ Agent 4: Compliance
    ↓
Response Aggregation
    ↓
HTTP Response (JSON)
    ↓
Result Display (Streamlit UI)
```

### Batch Processing Flow
```
JSON Upload (Streamlit)
    ↓
File Parsing
    ↓
For Each Application:
    ├→ HTTP POST Request
    ├→ Orchestrator Pipeline
    └→ Result Collection
    ↓
Aggregate Statistics
    ↓
Display Summary & Details
```

## Error Handling

### Request Validation
- Empty fields → 400 Bad Request
- Type mismatches → 400 Bad Request
- Out-of-range values → 400 Bad Request

### Agent Errors
- Calculation errors → Logged and handled gracefully
- Missing data → Default values applied

### API Errors
- Connection errors → User notification
- Timeout (>10s) → Retry logic
- 5xx errors → Error message returned

## Performance Considerations

### Response Time
- Single application: 100-500ms
- Batch (10 applications): 1-2 seconds
- Batch (100 applications): 10-15 seconds

### Scalability
- Horizontal scaling: Deploy multiple FastAPI instances
- Load balancer: Nginx or similar
- Agent isolation: No shared state between requests

### Database (Future)
- Application history: PostgreSQL
- Decision audit trail: MongoDB
- Caching layer: Redis for frequent lookups

## Security Measures

1. **API Key Management**
   - Environment variables for secrets
   - No hardcoded credentials
   - Anthropic API key in .env

2. **Input Validation**
   - Pydantic strict mode
   - Type checking
   - Range validation

3. **Error Handling**
   - No sensitive data in errors
   - Generic error messages to users
   - Detailed logging for debugging

4. **CORS**
   - Allow-origin configuration
   - Development: Allow all (*)
   - Production: Specific domains

## Monitoring & Logging

### Metrics to Track
- Request count by endpoint
- Average response time
- Decision distribution (Approved/Rejected/Review)
- Error rate
- Agent-specific metrics

### Logs
- Request/response logging
- Agent execution time
- Decision rationale
- Error traces

## Future Enhancements

1. **LLM Integration**
   - Use Claude for natural language explanations
   - Dynamic risk assessment
   - Pattern recognition for anomalies

2. **Advanced Features**
   - Document verification via vision API
   - Real-time credit score updates
   - Machine learning model integration
   - Complex approval workflows

3. **Infrastructure**
   - Database for persistence
   - Message queues for async processing
   - Webhooks for external integrations
   - Admin dashboard

4. **Compliance**
   - Audit logging
   - Data retention policies
   - GDPR/CCPA compliance
   - Fair lending rules

## Testing Strategy

### Unit Tests
- Agent calculation functions
- Risk scoring algorithms
- Decision logic

### Integration Tests
- API endpoint testing
- Multi-agent workflow
- Error handling

### Load Tests
- Single application performance
- Batch processing throughput
- Concurrent request handling

### Acceptance Tests
- Business logic validation
- User workflows
- Edge cases

## Deployment Architecture

### Local Development
```
python3 fastapi_service.py  (Port 8000)
streamlit run streamlit_app.py  (Port 8501)
```

### Docker Containerized
```
Docker Image: loan-approval:latest
Container: fastapi (8000)
Container: streamlit (8501)
Shared Volume: Application code
```

### Cloud Deployment (AWS Example)
```
ECS Cluster
  ├→ FastAPI Service (ECS Task)
  ├→ Streamlit Service (ECS Task)
  ├→ ALB (Application Load Balancer)
  ├→ RDS (PostgreSQL for persistence)
  └→ S3 (Logs & artifacts)
```

## Summary

This architecture provides:
- **Modularity**: Independent agents with clear responsibilities
- **Scalability**: Horizontal scaling capabilities
- **Explainability**: Transparent decision-making process
- **Maintainability**: Clean separation of concerns
- **Extensibility**: Easy to add new agents or features
