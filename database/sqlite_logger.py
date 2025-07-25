import sqlite3
from pathlib import Path
from datetime import datetime

DB_DIR = Path("database")
DB_DIR.mkdir(parents=True, exist_ok=True)  # 🔧 Ensure folder exists

DB_FILE = DB_DIR / "incidents.db"

class Logger:
    def __init__(self):
        self.conn = sqlite3.connect(DB_FILE, check_same_thread=False)
        self._init_db()

    def _init_db(self):
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                operator_id TEXT NOT NULL,
                task_name TEXT NOT NULL,
                start_time TEXT,
                end_time TEXT,
                total_score REAL DEFAULT 0.0,
                max_score REAL DEFAULT 0.0
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS hazards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                hazard_type TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                description TEXT,
                FOREIGN KEY(session_id) REFERENCES sessions(session_id)
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hazard_id INTEGER NOT NULL,
                action TEXT NOT NULL,
                reward INTEGER,
                classification TEXT,
                timestamp TEXT NOT NULL,
                FOREIGN KEY(hazard_id) REFERENCES hazards(id)
            )
        """)
        self.conn.commit()

    def start_session(self, session_id, operator_id, task_name):
        cur = self.conn.cursor()
        cur.execute("""
            INSERT OR REPLACE INTO sessions (session_id, operator_id, task_name, start_time)
            VALUES (?, ?, ?, ?)
        """, (session_id, operator_id, task_name, datetime.utcnow().isoformat()))
        self.conn.commit()

    def log_hazard(self, session_id, hazard_type, description):
        cur = self.conn.cursor()
        cur.execute("""
            INSERT INTO hazards (session_id, hazard_type, timestamp, description)
            VALUES (?, ?, ?, ?)
        """, (session_id, hazard_type, datetime.utcnow().isoformat(), description))
        self.conn.commit()
        return cur.lastrowid

    def log_action(self, hazard_id, action, reward, classification):
        cur = self.conn.cursor()
        cur.execute("""
            INSERT INTO actions (hazard_id, action, reward, classification, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (hazard_id, action, reward, classification, datetime.utcnow().isoformat()))
        self.conn.commit()

    def end_session(self, session_id, total_score, max_score):
        cur = self.conn.cursor()
        cur.execute("""
            UPDATE sessions
            SET end_time = ?, total_score = ?, max_score = ?
            WHERE session_id = ?
        """, (datetime.utcnow().isoformat(), total_score, max_score, session_id))
        self.conn.commit()
