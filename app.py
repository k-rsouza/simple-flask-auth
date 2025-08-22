from flask import Flask, jsonify, request
from models.user import User
from database import db
from flask_login import LoginManager, login_user, current_user


app = Flask(__name__)
app.config['SECRET_KEY'] = "key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'    # config fixa para caminho do banco

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

    print("Recebido:", username, password)

    if username and password:
        user = User.query.filter_by(username=username).first()   # (Recupera em formato de lista) filter() ou filter_by() | first() recupera o primeiro, pode se usar all() para recuperar todos os objetos
        print("User encontrado:", user)
        if user and user.password == password:
            login_user(user)
            print(current_user.is_authenticated)
            return jsonify({"message":"Autenticação realizada com sucesso!"})
    
    return jsonify({"message": "Credenciais inválidas..."}), 400
                    

@app.route("/hello-world", methods=["GET"])
def hello_world():
    return "Hello World"

if __name__ == '__main__':
    app.run(debug=True)

