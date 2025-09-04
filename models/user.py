from database import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    # id (int), Username(text), password (text)
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)     # nullable -> equivalente de NULL ou NOTNULL no SQL
    password = db.Column(db.String(80), nullable=False)      # Sem unique pois podem haver senhas iguais entre os usuarios do db, diferentemente do username
    role = db.Column(db.String(80), nullable=False, default='user')