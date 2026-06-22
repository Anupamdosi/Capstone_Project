#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}"
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║   Agentic AI Intelligent Loan Approval System             ║"
echo "║   Startup Script                                          ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed.${NC}"
    exit 1
fi

echo -e "${YELLOW}[1/4] Checking Python version...${NC}"
python3 --version

echo -e "${YELLOW}[2/4] Installing dependencies...${NC}"
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to install dependencies.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Dependencies installed${NC}"

echo -e "${YELLOW}[3/4] Starting FastAPI service...${NC}"
echo -e "${GREEN}FastAPI will run on http://localhost:8000${NC}"
python3 fastapi_service.py &
FASTAPI_PID=$!

sleep 2

echo -e "${YELLOW}[4/4] Starting Streamlit UI...${NC}"
echo -e "${GREEN}Streamlit will open on http://localhost:8501${NC}"
streamlit run streamlit_app.py

# Cleanup
trap "kill $FASTAPI_PID" EXIT
