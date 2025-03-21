from run import *
from flask import render_template

@app.route('/')
def home():
    username = session.get('username') 
    return render_template('home.html', username=username)

@app.route('/contact')
def contacts():
    return render_template("contact.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    criar_tabela()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            session['username'] = username  
            return redirect(url_for('home'))  
        else:
            return 'Usuário ou senha incorretos.'
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    criar_tabela()
    if request.method == 'POST':
        new_username = request.form['new_username']
        new_password = request.form['new_password']
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO usuarios (username, password) VALUES (?, ?)', (new_username, new_password))
            conn.commit()
            conn.close()
            return 'Cadastro bem-sucedido!'
        except sqlite3.IntegrityError:
            return 'Nome de usuário já existe.'
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/perfil/<user>')
def perfil(user):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE username = ?', (user,))
    user_data = cursor.fetchone()
    conn.close()
    if user_data:
        user_dict = {'username': user_data[1], 'password': user_data[2], 'email': user_data[3]}
        return render_template('perfil.html', user=user_dict)
    else:
        return "Usuário não encontrado."

@app.route('/update_perfil')
def update_perfil():
    if 'username' in session:
        username = session['username']
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE username = ?', (username,))
        user_data = cursor.fetchone()
        conn.close()
        if user_data:
            user_dict = {'username': user_data[1], 'password': user_data[2], 'email': user_data[3]}
            return render_template('update_perfil.html', user=user_dict)
        else:
            return 'Usuário não encontrado.'
    else:
        return redirect(url_for('login'))

@app.route('/atualizar_perfil', methods=['POST'])
def atualizar_perfil():
    if 'username' in session:
        username = session['username']
        new_username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()

        if password:
            cursor.execute('UPDATE usuarios SET username = ?, email = ?, password = ? WHERE username = ?', (new_username, email, password, username))
        else:
            cursor.execute('UPDATE usuarios SET username = ?, email = ? WHERE username = ?', (new_username, email, username))

        conn.commit()
        conn.close()

        if new_username != username:
            session['username'] = new_username

        return redirect(url_for('perfil', user=new_username))
    else:
        return redirect(url_for('login'))