from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager

from model import User, db
from routes import api_blueprint

app = Flask(__name__)
app.config['SECRET_KEY'] = "minha_chave_123"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'


db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'api.login'
CORS(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


app.register_blueprint(api_blueprint)

if __name__ == "__main__":
    with app.app_context():
        # Cria as tabelas no MySQL automaticamente
        db.create_all()
    app.run(debug=True)