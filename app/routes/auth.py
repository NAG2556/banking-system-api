from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from ..models.db import db
from ..models.user import User

auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password are required'}), 400

    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'User already exists'}), 409

    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, password_hash=hashed_pw)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully', 'user_id': new_user.id}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password are required'}), 400

    user = User.query.filter_by(username=data.get('username')).first()
    if not user or not bcrypt.check_password_hash(user.password_hash, data.get('password')):
        return jsonify({'error': 'Invalid username or password'}), 401

    access_token = create_access_token(identity=str(user.id))
    return jsonify({'access_token': access_token}), 200
