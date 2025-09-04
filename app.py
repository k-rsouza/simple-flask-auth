import bcrypt
from flask import Flask, jsonify, request
from models.user import User
from database import db
from flask_login import LoginManager, login_user, current_user, logout_user, login_required


app = Flask(__name__)
app.config['SECRET_KEY'] = "key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@127.0.0.1:3306/flask-crud'    # config fixa para caminho do banco

login_manager = LoginManager()
db.init_app(app) 
'''
inicializando a variavel db no app, pois as app.configs estão aqui,
dessa forma podemos manter a criação do banco de dados em uma classe separada, e apenas 
instancia-la aqui no app. Evitando um erro de importação circular
'''
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/login', methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        user = User.query.filter_by(username=username).first()   # (Recupera em formato de lista) filter() ou filter_by() | first() recupera o primeiro, pode se usar all() para recuperar todos os objetos
        
        if user and bcrypt.checkpw(str.encode(password), str.encode(user.password)):
            login_user(user)
            print(current_user.is_authenticated)
            return jsonify({"message":"Autenticação realizada com sucesso!"})
    
    return jsonify({"message": "Credenciais inválidas..."}), 400


@app.route('/logout', methods=['GET'])
@login_required   # Decorador que protege a rota de usuarios não autenticados, deve ficar entre a rota e a função
def logout():
    logout_user()
    return jsonify({"message": "Logout realizado com sucesso!"})


@app.route('/user', methods=["POST"])
# Poderia proteger esta rota com @login_required, assim somente usuarios autenticados poderiam criar novos usuarios
def create_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        hashed_password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())     # Criptografando a senha com a biblioteca BCrypt do Python, e a função Hashed da mesma
        user = User(username=username, password=hashed_password, role='user')
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "Usuário cadastrado com sucesso!"})

    return jsonify({"message": "Dados Inválidos!"}), 400

@app.route('/user/<int:id_user>', methods=["GET"])
@login_required
def read_user(id_user):
    user = User.query.get(id_user)
    if user:
        return {"username": user.username}
    
    return jsonify({"message": "Usuário não encontrado..."}), 404

@app.route('/user/<int:id_user>', methods=["PUT"])
@login_required
def update_user(id_user):
    data = request.json
    user = User.query.get(id_user)

    if id_user != current_user.id and current_user.role == "user":
        return jsonify({"message": "Operação não permitida!"}), 403
    
    if user and data.get("password"):
        user.password = data.get("password")
        db.session.commit(
            
        )
        return jsonify({"message": f"Usuário {id_user} atualizado com sucesso!"})
    
    return jsonify({"message": "Usuário não encontrado..."})

@app.route('/user/<int:id_user>', methods=["DELETE"])
@login_required
def delete_user(id_user):
    user = User.query.get(id_user)

    if current_user.role != 'admin':
        return jsonify({"message": "Operação não permitida!"}), 403
    if id_user == current_user.id:
        return jsonify({"message": "Deleção não permitida!!!"}), 403   # O usuário não pode deletar a si mesmo se não o sistema fica inacessível...

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"Usuário {id_user} deletado com sucesso!"})
    
    return jsonify({"message": "Usuário não encontrado..."}), 404

@app.route("/hello-world", methods=["GET"])
def hello_world():
    return "Hello World"

if __name__ == '__main__':
    app.run(debug=True)

