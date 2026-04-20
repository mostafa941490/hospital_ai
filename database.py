import sqlite3
import pandas as pd
import os

DB_NAME = "hospital.db"

def init_db():
    """Initialize the SQLite database and create tables if they don't exist."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            glucose REAL,
            bp REAL,
            bmi REAL,
            insulin REAL,
            ml_score REAL,
            risk_level TEXT,
            ai_insight TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_patient(name, age, glucose, bp, bmi, insulin, score, risk, insight):
    """Save a patient record to the database."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO patients (name, age, glucose, bp, bmi, insulin, ml_score, risk_level, ai_insight)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, age, glucose, bp, bmi, insulin, score, risk, insight))
    conn.commit()
    conn.close()

def get_all_patients():
    """Retrieve all patient records for analytics."""
    if not os.path.exists(DB_NAME):
        return pd.DataFrame()
    conn = sqlite3.connect(DB_NAME)
    try:
        df = pd.read_sql_query("SELECT * FROM patients ORDER BY timestamp DESC", conn)
    except:
        df = pd.DataFrame()
    conn.close()
    return df
