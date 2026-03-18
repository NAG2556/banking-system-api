from flask import Flask, jsonify
from flask_cors import CORS
from .config import Config
from .models.db import db
from flask_jwt_extended import JWTManager

jwt = JWTManager()

def create_app():
    app = Flask(__name__, static_folder='../frontend', static_url_path='/')
    CORS(app)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        from .models.user import User
        from .models.account import Account
        from .models.transaction import Transaction
        db.create_all()

    from .routes.auth import auth_bp
    from .routes.accounts import accounts_bp
    from .routes.transactions import transactions_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(accounts_bp, url_prefix='/api/accounts')
    app.register_blueprint(transactions_bp, url_prefix='/api/transactions')

    @app.route('/')
    def home():
        return app.send_static_file('index.html')

    return app
