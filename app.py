from flask import Flask, request, jsonify
from models.user import User 
from database import db
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
import bcrypt
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login'

migrate = Migrate(app, db)

@app.route('/')
def home():
    return jsonify({"message": "API Flask funcionando!"})

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # Certifique-se de converter o ID para inteiro

@app.route('/login', methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            login_user(user)
            return jsonify({"message": "Autenticação realizada com sucesso"})

    return jsonify({"message": "Credenciais inválidas"}), 400

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout realizado com sucesso!"})

@app.route('/user', methods=["POST"])
def create_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user = User(username=username, password=hashed_password, role='user')
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "Usuário cadastrado com sucesso"})

    return jsonify({"message": "Dados inválidos"}), 400

@app.route('/user/<int:id_user>', methods=["GET"])
@login_required
def read_user(id_user):
    user = User.query.get(id_user)

    if user:
        return jsonify({"username": user.username, "role": user.role})

    return jsonify({"message": "Usuário não encontrado"}), 404

@app.route('/user/<int:id_user>', methods=["PUT"])
@login_required
def update_user(id_user):
    data = request.json
    user = User.query.get(id_user)

    if not user:
        return jsonify({"message": "Usuário não encontrado"}), 404

    if id_user != current_user.id and current_user.role == "user":
        return jsonify({"message": "Operação não permitida"}), 403

    if data.get("password"):
        hashed_password = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        return jsonify({"message": f"Usuário {id_user} atualizado com sucesso"})

    return jsonify({"message": "Nenhum dado atualizado"}), 400

@app.route('/user/<int:id_user>', methods=["DELETE"])
@login_required
def delete_user(id_user):
    user = User.query.get(id_user)

    if not user:
        return jsonify({"message": "Usuário não encontrado"}), 404

    if current_user.role != 'admin':
        return jsonify({"message": "Operação não permitida"}), 403

    if id_user == current_user.id:
        return jsonify({"message": "Deleção não permitida"}), 403

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"Usuário {id_user} deletado com sucesso"})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Garante que as tabelas sejam criadas antes de rodar o servidor
    app.run(debug=True)

