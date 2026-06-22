"""Pytest configuration and fixtures."""

import pytest
import sqlite3
import os
from agents import ApplicantData


@pytest.fixture(scope="session")
def test_db():
    """Create test database."""
    db_path = "test_loan_applications.db"
    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS loan_applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            applicant_id TEXT NOT NULL,
            age INTEGER,
            income REAL,
            employment_type TEXT,
            credit_score INTEGER,
            loan_amount REAL,
            tenure_months INTEGER,
            existing_liabilities REAL,
            location TEXT,
            decision TEXT,
            risk_score REAL,
            confidence_level TEXT,
            explanation TEXT,
            case_id TEXT,
            timestamp TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    yield db_path
    conn.close()

    # Cleanup
    if os.path.exists(db_path):
        os.remove(db_path)


@pytest.fixture
def sample_applicant_data():
    """Sample applicant data for testing."""
    return ApplicantData(
        applicant_id="APP-TEST-001",
        age=35,
        income=750000.0,
        employment_type="Employed",
        credit_score=720,
        loan_amount=2500000.0,
        tenure_months=180,
        existing_liabilities=500000.0,
        location="India"
    )


@pytest.fixture
def low_risk_applicant():
    """Low risk applicant for testing."""
    return ApplicantData(
        applicant_id="APP-LOW-RISK",
        age=40,
        income=1500000.0,
        employment_type="Employed",
        credit_score=800,
        loan_amount=1000000.0,
        tenure_months=240,
        existing_liabilities=100000.0,
        location="India"
    )


@pytest.fixture
def high_risk_applicant():
    """High risk applicant for testing."""
    return ApplicantData(
        applicant_id="APP-HIGH-RISK",
        age=25,
        income=300000.0,
        employment_type="Self-employed",
        credit_score=550,
        loan_amount=3000000.0,
        tenure_months=60,
        existing_liabilities=2000000.0,
        location="India"
    )


@pytest.fixture
def medium_risk_applicant():
    """Medium risk applicant for testing."""
    return ApplicantData(
        applicant_id="APP-MED-RISK",
        age=45,
        income=850000.0,
        employment_type="Business Owner",
        credit_score=680,
        loan_amount=2000000.0,
        tenure_months=180,
        existing_liabilities=750000.0,
        location="India"
    )
