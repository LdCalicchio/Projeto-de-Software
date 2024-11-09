from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt

app = Flask(__name__)
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
    
@app.route('/sucesso')
def sucesso():
    return render_template('sucesso.html')

if __name__ == '__main__':
    app.run(debug=True)