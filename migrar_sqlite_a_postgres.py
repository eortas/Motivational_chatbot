import sqlite3
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
POSTGRES_URL = os.getenv("DATABASE_URL")

# 📥 Leer datos desde historico.db (SQLite)
sqlite_conn = sqlite3.connect("historico.db")
sqlite_cursor = sqlite_conn.cursor()
sqlite_cursor.execute("SELECT fecha, estado, respuesta FROM interacciones")
registros = sqlite_cursor.fetchall()
sqlite_conn.close()

# 🚚 Insertar en PostgreSQL
postgres_conn = psycopg2.connect(POSTGRES_URL)
postgres_cursor = postgres_conn.cursor()

# Crear tabla si no existe (por seguridad)
postgres_cursor.execute('''
    CREATE TABLE IF NOT EXISTS interacciones (
        id SERIAL PRIMARY KEY,
        fecha TIMESTAMP,
        estado TEXT,
        respuesta TEXT
    )
''')

# Insertar registros
for fecha, estado, respuesta in registros:
    postgres_cursor.execute(
        "INSERT INTO interacciones (fecha, estado, respuesta) VALUES (%s, %s, %s)",
        (fecha, estado, respuesta)
    )

postgres_conn.commit()
postgres_conn.close()

print(f"✅ Migrados {len(registros)} registros a PostgreSQL.")