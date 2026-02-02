import sqlite3

DB_NAME = "ranking.db"

def criar_banco():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS ranking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            pontuacao INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def salvar_pontuacao(nome, pontuacao):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO ranking (nome, pontuacao) VALUES (?, ?)", (nome, pontuacao))
    conn.commit()
    conn.close()

def ler_ranking(top=10):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT nome, pontuacao FROM ranking ORDER BY pontuacao DESC LIMIT ?", (top,))
    resultados = c.fetchall()
    conn.close()
    return resultados
