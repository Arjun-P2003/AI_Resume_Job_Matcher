
import sqlite3
import json
from datetime import datetime


DATABASE_NAME = "resume_history.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def create_table():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analysis_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resume_filename TEXT,
            job_description TEXT,
            similarity_score REAL,
            skill_match_percentage REAL,
            matched_skills TEXT,
            missing_skills TEXT,
            analysis_date TEXT
        )
    """)

    connection.commit()
    connection.close()


def save_analysis(
    resume_filename,
    job_description,
    similarity_score,
    skill_match_percentage,
    matched_skills,
    missing_skills
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO analysis_history (
            resume_filename,
            job_description,
            similarity_score,
            skill_match_percentage,
            matched_skills,
            missing_skills,
            analysis_date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        resume_filename,
        job_description,
        similarity_score,
        skill_match_percentage,
        json.dumps(matched_skills),
        json.dumps(missing_skills),
        datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    ))

    connection.commit()
    connection.close()


def get_analysis_history():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM analysis_history
        ORDER BY id DESC
    """)

    records = cursor.fetchall()
    connection.close()

    return records
