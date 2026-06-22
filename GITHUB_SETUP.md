# GitHub Setup & Deployment Guide

## Quick GitHub Setup

### 1. Create GitHub Repository

1. Go to [GitHub.com](https://github.com/new)
2. Repository name: `agentic-loan-approval`
3. Description: "AI-powered multi-agent system for intelligent loan approval decisions"
4. Visibility: Public
5. Click "Create repository"

### 2. Push Local Repository to GitHub

```bash
# Navigate to project directory
cd /home/ubuntu/Desktop/demo

# Add remote origin (replace USERNAME with your GitHub username)
git remote add origin https://github.com/USERNAME/agentic-loan-approval.git

# Verify remote
git remote -v

# Push to GitHub
git branch -M main
git push -u origin main
```

### 3. GitHub Repository URL

Once pushed, your repository will be available at:
```
https://github.com/USERNAME/agentic-loan-approval
```

## Repository Structure on GitHub

Your GitHub repository will contain:

```
agentic-loan-approval/
├── README.md                              # Main documentation
├── ARCHITECTURE.md                        # System architecture details
├── CONTRIBUTING.md                        # Contribution guidelines
├── GITHUB_SETUP.md                       # This file
├── LICENSE                                # MIT License (optional)
├── case_study_agentic_loan_approval.md   # Business case study
├── agents.py                              # Agent implementations
├── fastapi_service.py                    # FastAPI microservice
├── streamlit_app.py                      # Streamlit UI
├── requirements.txt                      # Python dependencies
├── Dockerfile                             # Docker image definition
├── docker-compose.yml                    # Docker Compose configuration
├── start.sh                               # Startup script
├── sample_data.json                      # Sample test data
├── .gitignore                            # Git ignore rules
├── .env.example                          # Environment template
└── main.ipynb                            # Original notebook (optional)
```

## Adding to GitHub (Step by Step)

### Option A: SSH Authentication (Recommended)

1. **Generate SSH Key** (if you haven't already):
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
# Press Enter for all prompts (or set custom passphrase)
```

2. **Add SSH Key to GitHub**:
- Copy: `cat ~/.ssh/id_ed25519.pub`
- Go to GitHub Settings → SSH and GPG keys
- Click "New SSH key"
- Paste the key

3. **Update Remote**:
```bash
git remote set-url origin git@github.com:USERNAME/agentic-loan-approval.git
```

4. **Push**:
```bash
git push -u origin main
```

### Option B: HTTPS Authentication

1. **Create Personal Access Token**:
- GitHub Settings → Developer settings → Personal access tokens
- Generate new token with `repo` scope
- Copy the token

2. **Push with Token**:
```bash
git push -u origin main
# When prompted for password, paste the token
```

## Repository Settings

### 1. Branch Protection (Optional)
- Go to Settings → Branches
- Add rule for `main` branch
- Require pull request reviews before merging

### 2. Enable GitHub Actions (CI/CD)
- Settings → Actions → General
- Allow actions to create pull requests

### 3. Add Topics
- In repository About section, add topics:
  - `agentic-ai`
  - `loan-approval`
  - `multi-agent`
  - `fastapi`
  - `streamlit`
  - `langgraph`

### 4. Add Repository Description
Edit About section:
```
AI-powered multi-agent system for intelligent loan approval decisions. 
Featuring FastAPI backend, Streamlit UI, and LangGraph orchestration.
```

## Add License

```bash
# Create MIT License file
cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2024 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
...
EOF

git add LICENSE
git commit -m "Add MIT License"
git push origin main
```

## Add .env.example

```bash
cp .env .env.example
# Edit .env.example to remove actual API key
echo "ANTHROPIC_API_KEY=your_api_key_here" > .env.example
git add .env.example
git commit -m "Add environment template"
git push origin main
```

## Setup GitHub Actions CI/CD

Create `.github/workflows/test.yml`:

```yaml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Lint with flake8
      run: |
        pip install flake8
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
    
    - name: Type check with mypy
      run: |
        pip install mypy
        mypy --ignore-missing-imports agents.py fastapi_service.py streamlit_app.py || true
```

## Deployment Options

### Option 1: Deploy with Heroku

```bash
# Login to Heroku
heroku login

# Create Heroku app
heroku create your-app-name

# Add Procfile
cat > Procfile << 'EOF'
web: python fastapi_service.py
worker: streamlit run streamlit_app.py
EOF

# Set environment variables
heroku config:set ANTHROPIC_API_KEY=your_key

# Deploy
git push heroku main
```

### Option 2: Deploy with AWS

See ARCHITECTURE.md for AWS deployment architecture.

**Quick Steps**:
1. Create ECR repository
2. Push Docker image
3. Create ECS cluster and task
4. Configure Application Load Balancer
5. Deploy services

### Option 3: Deploy with Docker Hub

```bash
# Login to Docker Hub
docker login

# Build image
docker build -t yourusername/agentic-loan-approval:latest .

# Push to Docker Hub
docker push yourusername/agentic-loan-approval:latest

# Anyone can now run:
docker run -p 8000:8000 -p 8501:8501 \
  -e ANTHROPIC_API_KEY=your_key \
  yourusername/agentic-loan-approval:latest
```

## Share Links for Your Manager

### GitHub Repository
```
https://github.com/USERNAME/agentic-loan-approval
```

### Live Demo (if deployed)
```
FastAPI API: https://your-domain:8000
Streamlit UI: https://your-domain:8501
```

### Documentation Links
```
README: https://github.com/USERNAME/agentic-loan-approval/blob/main/README.md
Architecture: https://github.com/USERNAME/agentic-loan-approval/blob/main/ARCHITECTURE.md
Case Study: https://github.com/USERNAME/agentic-loan-approval/blob/main/case_study_agentic_loan_approval.md
```

## Local Testing Before Push

```bash
# Test FastAPI
python3 fastapi_service.py &
sleep 2
curl http://localhost:8000/health

# Test Streamlit
streamlit run streamlit_app.py

# Test with sample data
python3 -c "
import requests
import json

with open('sample_data.json') as f:
    data = json.load(f)
    
for app in data[:1]:
    response = requests.post('http://localhost:8000/analyze_loan_application', json=app)
    print(json.dumps(response.json(), indent=2))
"
```

## Create README for Managers

Create a `MANAGER_README.md`:

```markdown
# Executive Summary

## Project: Agentic AI Intelligent Loan Approval System

### Overview
Automated loan approval system using multi-agent AI architecture.

### Key Features
- ✅ Fast processing (100-500ms per application)
- ✅ Explainable decisions with risk scores
- ✅ Batch processing capability
- ✅ Web UI and REST API
- ✅ Production-ready code

### Links
- GitHub: https://github.com/USERNAME/agentic-loan-approval
- Local Demo: http://localhost:8501
- API Docs: http://localhost:8000/docs

### Demo Test Data
See sample_data.json for example applications

### Technology Stack
- Backend: FastAPI + LangGraph
- Frontend: Streamlit
- AI: Anthropic Claude
- Deployment: Docker

### Success Metrics
- Decision accuracy: Rule-based validation
- Response time: <500ms per app
- Scalability: Handles 100+ apps/minute
- Explainability: Full reasoning for each decision
```

## Verify Everything is on GitHub

```bash
# Check remote
git remote -v

# Check branch
git branch -a

# Check log
git log --oneline

# List files tracked
git ls-files
```

## Final Checklist

- [ ] GitHub repository created
- [ ] Code pushed to main branch
- [ ] README visible and well-formatted
- [ ] License added
- [ ] Topics added
- [ ] Description updated
- [ ] .env.example added
- [ ] Docker files included
- [ ] Documentation complete
- [ ] Sample data included
- [ ] GitHub Actions (optional) configured
- [ ] Links ready to share

## Support & Questions

### If you get "remote origin already exists" error:
```bash
git remote remove origin
git remote add origin https://github.com/USERNAME/agentic-loan-approval.git
```

### If you need to update after changes:
```bash
git add .
git commit -m "Update: description of changes"
git push origin main
```

### For team collaboration:
```bash
# Pull latest changes
git pull origin main

# Create feature branch
git checkout -b feature/your-feature

# Make changes and commit
git push origin feature/your-feature

# Create Pull Request on GitHub
```

---

**Next Steps**:
1. Create GitHub repository
2. Push code to GitHub
3. Configure repository settings
4. Share links with manager
5. Monitor for feedback
6. Deploy if needed

Questions? Check ARCHITECTURE.md or README.md for more details.
