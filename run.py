from flask import Flask, request, redirect, url_for, session 
import sqlite3

app = Flask(__name__)
app.secret_key = 'chave_secreta'

from routes.routes import *

def criar_tabela():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT  -- Coluna email adicionada, sem restrição NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


if __name__ == "__main__":
    app.run()