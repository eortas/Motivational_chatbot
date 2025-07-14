import sqlite3
from datetime import datetime

DB_FILE = "historico.db"

def crear_tabla_si_no_existe():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interacciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            estado TEXT,
            respuesta TEXT
        )
    ''')
    conn.commit()
    conn.close()

def guardar_interaccion(estado, respuesta):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO interacciones (fecha, estado, respuesta) VALUES (?, ?, ?)",
        (datetime.now().isoformat(), estado, respuesta)
    )
    conn.commit()
    conn.close()

def cargar_historial():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT fecha, estado, respuesta FROM interacciones ORDER BY fecha DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def borrar_historial():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM interacciones")
    conn.commit()
    conn.close()