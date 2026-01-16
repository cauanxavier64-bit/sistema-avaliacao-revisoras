import sqlite3
import os

# Caminho absoluto da pasta onde está este arquivo (MEU_APP_PY)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "revisoras.db")

def conectar():
    return sqlite3.connect(DB_PATH)

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS revisoras (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT UNIQUE,
        ativa INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS avaliacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        revisora_id INTEGER,
        placa TEXT,
        pontos INTEGER,
        data_avaliacao DATE
    )
    """)

    conn.commit()
    conn.close()

