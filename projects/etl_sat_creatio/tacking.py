import os
import sqlite3
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

DB_PATH = os.path.join(os.getenv("DB_PATH"), "download_requests.db")
process_id = None


def init():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(""" 
        CREATE TABLE IF NOT EXISTS status_sync (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hora_inicio DATETIME,
            hora_fin DATETIME,
            status TEXT,
            num_registros_creatio INT,
            num_cfdi_sat INT
        )
    """)
    conn.commit()
    conn.close()


def register_process():
    init()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(""" 
        INSERT INTO status_sync (hora_inicio, status) 
        VALUES (?, ?) 
    """, (datetime.now(), "En ejecución"))
    global process_id
    process_id = c.lastrowid
    conn.commit()
    conn.close()


def register_start_tracking(num_cfdi_sat: int):
    init()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""  
        UPDATE status_sync
        SET num_cfdi_sat = ?
        WHERE id = ?
    """, (num_cfdi_sat, process_id))
    conn.commit()
    conn.close()


def register_load(num_registros_creatio: int):
    init()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""  
        UPDATE status_sync
        SET num_registros_creatio = ?
        WHERE id = ?
    """, (num_registros_creatio, process_id))
    conn.commit()
    conn.close()


def register_status(status: str):
    init()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(""" 
        UPDATE status_sync
        SET status = ?
        WHERE id = ?
    """, (status, process_id))
    conn.commit()
    conn.close()


def register_final_tracking():
    init()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(""" 
        UPDATE status_sync
        SET hora_fin = ?
        WHERE id = ?
        """, (datetime.now(), process_id))
    conn.commit()
    conn.close()
