from flask import Flask, jsonify
from .config import Config
from .models.db import db
from flask_jwt_extended import JWTManager

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
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
        return jsonify({
            "message": "Welcome to the Banking API!",
            "status": "online",
            "documentation": "Please refer to sample_requests.md for API documentation endpoints."
        })

    return app
