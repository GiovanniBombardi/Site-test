from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def criar_tabela():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()





if __name__ == '__main__':
    app.run()