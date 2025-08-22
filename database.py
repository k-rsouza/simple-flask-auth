from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()   # criando instancia do ORM e passando a classe como parametro
'''
SQLAlchemy é iniciado como uma instância, ao rodar o flask shell e create all
ele cria o banco de dados baseado em tudo que ele conseguiu enxergar pelo db model
'''
