# 🚀 Quick Start Guide

## ⚡ 2-Minute Setup

### Prerequisites
- Python 3.8+
- `pip` package manager
- Anthropic API Key (already in .env)

### Step 1: Install Dependencies (1 minute)
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application (1 minute)

**Terminal 1 - Start FastAPI Service:**
```bash
python3 fastapi_service.py
```

You'll see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**Terminal 2 - Start Streamlit UI:**
```bash
streamlit run streamlit_app.py
```

You'll see:
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

### Step 3: Open in Browser
- **UI**: http://localhost:8501
- **API Docs**: http://localhost:8000/docs

✅ You're ready to go!

---

## 📝 How to Use

### Submit a Single Application
1. Go to http://localhost:8501
2. Fill in the form with applicant details
3. Click "🚀 Analyze Application"
4. View the decision and reasoning

### Process Multiple Applications
1. Go to "📊 Batch Processing" tab
2. Upload a JSON file (try `sample_data.json`)
3. Click "Process Batch"
4. View all results and statistics

### View Analytics
1. Go to "📈 Analytics" tab
2. See decision distribution
3. View risk score histogram
4. Check summary statistics

---

## 🧪 Test with Sample Data

### Single Application via API
```bash
curl -X POST http://localhost:8000/analyze_loan_application \
  -H "Content-Type: application/json" \
  -d '{
    "applicant_id": "APP-001",
    "age": 35,
    "income": 75000,
    "employment_type": "Employed",
    "credit_score": 720,
    "loan_amount": 250000,
    "tenure_months": 180,
    "existing_liabilities": 50000,
    "location": "New York"
  }'
```

### Expected Response
```json
{
  "decision": "Approved",
  "risk_score": 35.5,
  "confidence_level": "High",
  "explanation": "Application approved. Risk score: 35.5/100. Strong financial profile.",
  "case_id": "CASE-APP-001-20240619102030",
  "timestamp": "2024-06-19T10:20:30.123456"
}
```

### Batch Processing
```bash
curl -X POST http://localhost:8000/batch_analyze \
  -H "Content-Type: application/json" \
  -d @sample_data.json
```

---

## 📊 Understanding Results

### Decision Types
- ✅ **Approved**: Applicant has strong financial profile (Risk < 30)
- ⚠️ **Manual Review**: Borderline case requiring human review (Risk 30-60)
- ❌ **Rejected**: High financial risk (Risk > 60)

### Risk Score
- 0-30: Low risk (typically approved)
- 30-60: Medium risk (manual review)
- 60-100: High risk (typically rejected)

### Key Factors
The response includes factors that influenced the decision:
- Income Stability
- Debt-to-Income Ratio
- Credit Risk Level
- Employment Risk

---

## 🔧 Troubleshooting

### Port Already in Use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Kill process on port 8501
lsof -ti:8501 | xargs kill -9
```

### API Connection Error
- Make sure FastAPI is running in Terminal 1
- Check http://localhost:8000/health

### Streamlit Cache Issues
```bash
# Clear Streamlit cache
streamlit cache clear

# Or start fresh
rm -rf .streamlit/cache
streamlit run streamlit_app.py
```

### Python Version Issues
```bash
# Check Python version
python3 --version  # Should be 3.8+

# Use specific version
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 📚 Next Steps

### 1. **Explore Documentation**
   - Read [README.md](README.md) for full overview
   - Check [ARCHITECTURE.md](ARCHITECTURE.md) for technical details
   - Review [MANAGER_DEMO.md](MANAGER_DEMO.md) for presentation tips

### 2. **Push to GitHub**
   - Follow [GITHUB_SETUP.md](GITHUB_SETUP.md)
   - Create repository: https://github.com/new
   - Push code and share links

### 3. **Deploy to Production**
   - Use Docker: `docker-compose up`
   - Deploy to cloud: AWS, Heroku, Google Cloud
   - Configure for production environment

### 4. **Integrate with Your Systems**
   - Use REST API for integration
   - Batch process your data
   - Monitor decisions

### 5. **Show Your Manager**
   - Use [MANAGER_DEMO.md](MANAGER_DEMO.md) as guide
   - Highlight business benefits
   - Share GitHub link

---

## 🎯 File Overview

| File | Purpose |
|------|---------|
| `agents.py` | Core agent implementations |
| `fastapi_service.py` | REST API server |
| `streamlit_app.py` | Web UI dashboard |
| `requirements.txt` | Python dependencies |
| `README.md` | Full documentation |
| `ARCHITECTURE.md` | System design details |
| `MANAGER_DEMO.md` | Presentation guide |
| `GITHUB_SETUP.md` | GitHub instructions |
| `sample_data.json` | Test data |
| `Dockerfile` | Docker image |
| `.env` | Configuration (API keys) |

---

## 💡 Example Use Cases

### Marketing Team
```bash
# Process list of loan applications
python3 -c "
import requests
import json

with open('sample_data.json') as f:
    apps = json.load(f)

for app in apps:
    r = requests.post('http://localhost:8000/analyze_loan_application', json=app)
    print(f\"{app['applicant_id']}: {r.json()['decision']}\")
"
```

### Compliance Officer
```bash
# Generate audit trail with case IDs
# Check timestamp and explanation for each decision
# Verify decision factors and risk scores
```

### System Administrator
```bash
# Monitor API health
curl http://localhost:8000/health

# Check container status (if using Docker)
docker ps

# Scale service (if needed)
docker-compose up --scale fastapi=3
```

---

## 🔐 Security Notes

1. **Never commit .env** (already in .gitignore)
2. **API key** stored in `.env` file
3. **CORS enabled** for development (configure for production)
4. **Input validation** via Pydantic
5. **Error handling** without exposing sensitive data

---

## 📞 Common Questions

**Q: Can I change the decision thresholds?**
A: Yes! Edit the `_make_decision()` method in `agents.py`

**Q: How do I add more agents?**
A: Create new agent class in `agents.py`, add to orchestration in `fastapi_service.py`

**Q: Can I use a database?**
A: Yes! Modify `fastapi_service.py` to add database integration

**Q: How do I deploy this?**
A: See ARCHITECTURE.md for deployment options (Docker, AWS, Heroku, etc.)

**Q: Can I use different LLM?**
A: Yes! Replace `anthropic` with your preferred LLM provider

---

## ✨ Tips for Success

1. **Start simple** - Try single application first
2. **Review decisions** - Check why decisions were made
3. **Test edge cases** - Try different applicant profiles
4. **Monitor performance** - Check response times
5. **Gather feedback** - Improve based on usage

---

**Ready to demo your manager?** 
→ Follow [MANAGER_DEMO.md](MANAGER_DEMO.md)

**Ready to deploy?**
→ Follow [ARCHITECTURE.md](ARCHITECTURE.md)

**Ready to share code?**
→ Follow [GITHUB_SETUP.md](GITHUB_SETUP.md)

---

**Status**: ✅ Running and Ready
**Version**: 1.0.0
**Last Updated**: June 2024
