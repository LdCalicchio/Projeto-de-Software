from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Chave secreta para gerenciar sessões
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '@349756Lu'
app.config['MYSQL_DB'] = 'plataforma_streaming'

mysql = MySQL(app)
bcrypt = Bcrypt(app)

@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'GET':
        return render_template('cadastro.html')
    elif request.method == 'POST':
        data = request.get_json()
        if not data:
            return jsonify({'message': 'Nenhum dado recebido.'}), 400
        
        try:
            # Hash da senha
            hashed_senha = bcrypt.generate_password_hash(data['senha']).decode('utf-8')
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)", (data['nome'], data['email'], hashed_senha))
            mysql.connection.commit()
            cur.close()
            return jsonify({'message': 'Usuário cadastrado com sucesso!'}), 201
        except Exception as e:
            return jsonify({'message': 'Erro ao cadastrar usuário.', 'error': str(e)}), 500

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        data = request.get_json()
        if not data:
            return jsonify({'message': 'Nenhum dado recebido.'}), 400
        
        try:
            email = data['email']
            senha = data['senha']
            cur = mysql.connection.cursor()
            cur.execute("SELECT id, nome, email, senha FROM usuarios WHERE email = %s", [email])
            user = cur.fetchone()
            cur.close()
            
            if user and bcrypt.check_password_hash(user[3], senha):
                session['user_id'] = user[0]
                session['user_name'] = user[1]
                return jsonify({'message': 'Login bem-sucedido!'}), 200
            else:
                return jsonify({'message': 'Email ou senha incorretos.'}), 401
        
        except Exception as e:
            return jsonify({'message': 'Erro ao tentar logar.', 'error': str(e)}), 500

@app.route('/log_sucesso')
def log_sucesso():
    return render_template('log_sucesso.html')

@app.route('/cad_sucesso')
def sucesso():
    return render_template('cad_sucesso.html')

if __name__ == '__main__':
    app.run(debug=True)