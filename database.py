"""Database management for loan application history."""

import sqlite3
import json
from datetime import datetime
from pathlib import Path

DATABASE_FILE = "loan_applications.db"


def init_database():
    """Initialize SQLite database."""
    conn = sqlite3.connect(DATABASE_FILE)
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
    conn.close()


def save_application(applicant_data: dict, decision_result: dict) -> bool:
    """Save loan application and decision to database."""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO loan_applications (
                applicant_id, age, income, employment_type, credit_score,
                loan_amount, tenure_months, existing_liabilities, location,
                decision, risk_score, confidence_level, explanation, case_id, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            applicant_data.get("applicant_id"),
            applicant_data.get("age"),
            applicant_data.get("income"),
            applicant_data.get("employment_type"),
            applicant_data.get("credit_score"),
            applicant_data.get("loan_amount"),
            applicant_data.get("tenure_months"),
            applicant_data.get("existing_liabilities"),
            applicant_data.get("location"),
            decision_result.get("decision"),
            decision_result.get("risk_score"),
            decision_result.get("confidence_level"),
            decision_result.get("explanation"),
            decision_result.get("case_id"),
            decision_result.get("timestamp")
        ))

        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving application: {e}")
        return False


def get_statistics():
    """Get summary statistics from database."""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()

        # Total applications
        cursor.execute("SELECT COUNT(*) FROM loan_applications")
        total = cursor.fetchone()[0]

        # Decision breakdown
        cursor.execute("""
            SELECT decision, COUNT(*) as count
            FROM loan_applications
            GROUP BY decision
        """)
        decisions = dict(cursor.fetchall())

        # Average risk score
        cursor.execute("SELECT AVG(risk_score) FROM loan_applications")
        avg_risk = cursor.fetchone()[0]

        conn.close()

        return {
            "total_processed": total,
            "approved": decisions.get("Approved", 0),
            "rejected": decisions.get("Rejected", 0),
            "manual_review": decisions.get("Requires Manual Review", 0),
            "average_risk_score": round(avg_risk, 2) if avg_risk else 0,
            "decisions_breakdown": decisions
        }
    except Exception as e:
        print(f"Error getting statistics: {e}")
        return {
            "total_processed": 0,
            "approved": 0,
            "rejected": 0,
            "manual_review": 0,
            "average_risk_score": 0,
            "decisions_breakdown": {}
        }


def get_all_applications(limit: int = 100):
    """Get all applications from database."""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM loan_applications
            ORDER BY created_at DESC
            LIMIT ?
        """, (limit,))

        results = cursor.fetchall()
        conn.close()

        return [dict(row) for row in results]
    except Exception as e:
        print(f"Error fetching applications: {e}")
        return []


def get_decision_distribution():
    """Get decision distribution for charts."""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT decision, COUNT(*) as count
            FROM loan_applications
            GROUP BY decision
            ORDER BY count DESC
        """)

        results = cursor.fetchall()
        conn.close()

        return {decision: count for decision, count in results}
    except Exception as e:
        print(f"Error getting distribution: {e}")
        return {}


def get_risk_scores():
    """Get all risk scores for distribution chart."""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()

        cursor.execute("SELECT risk_score FROM loan_applications WHERE risk_score IS NOT NULL")
        results = cursor.fetchall()
        conn.close()

        return [row[0] for row in results]
    except Exception as e:
        print(f"Error getting risk scores: {e}")
        return []


def export_to_json(filename: str = "loan_data_export.json") -> str:
    """Export all data to JSON file."""
    try:
        applications = get_all_applications(limit=None)
        stats = get_statistics()

        export_data = {
            "export_timestamp": datetime.now().isoformat(),
            "statistics": stats,
            "applications": applications
        }

        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)

        return filename
    except Exception as e:
        print(f"Error exporting data: {e}")
        return None


def export_to_csv(filename: str = "loan_data_export.csv") -> str:
    """Export data to CSV file."""
    try:
        import csv

        applications = get_all_applications(limit=None)

        if not applications:
            return None

        keys = applications[0].keys()

        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(applications)

        return filename
    except Exception as e:
        print(f"Error exporting to CSV: {e}")
        return None


def clear_all_data():
    """Clear all data from database."""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM loan_applications")
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error clearing data: {e}")
        return False


def delete_by_case_id(case_id: str) -> bool:
    """Delete a specific application by case ID."""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM loan_applications WHERE case_id = ?", (case_id,))
        conn.commit()
        conn.close()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error deleting application: {e}")
        return False


def get_application_by_case_id(case_id: str) -> dict:
    """Get specific application by case ID."""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM loan_applications WHERE case_id = ?", (case_id,))
        result = cursor.fetchone()
        conn.close()

        return dict(result) if result else None
    except Exception as e:
        print(f"Error fetching application: {e}")
        return None
