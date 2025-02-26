from database import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)  # Aumentei para 255 caracteres
    role = db.Column(db.String(20), nullable=False, default='user')  # Adicionando role
