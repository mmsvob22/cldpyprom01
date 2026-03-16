import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent.parent / "cldpyprom01.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS Resource (
            id                   INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name           TEXT NOT NULL,
            middle_name          TEXT,
            last_name            TEXT NOT NULL,
            company              TEXT,
            alloc_work_hours     INTEGER,
            alloc_max_hours      INTEGER,
            alloc_night_work     INTEGER,
            alloc_overtime       INTEGER,
            alloc_weekend        INTEGER,
            contact_title        TEXT,
            contact_mobile_phone TEXT,
            contact_fixed_line   TEXT,
            contact_email        TEXT,
            contact_post_code    TEXT,
            contact_other_info   TEXT,
            contact_street       TEXT,
            contact_city         TEXT,
            contact_province     TEXT,
            contact_country      TEXT,
            updated_by           TEXT,
            date_updated         TEXT,
            created_by           TEXT NOT NULL,
            date_created         TEXT NOT NULL,
            last_capacity_date   TEXT,
            last_cost_month      TEXT,
            registration_status  TEXT
        )
    """)
    conn.commit()
    conn.close()
