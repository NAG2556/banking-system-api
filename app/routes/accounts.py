from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.db import db
from ..models.account import Account

accounts_bp = Blueprint('accounts', __name__)

@accounts_bp.route('/', methods=['POST'])
@jwt_required()
def create_account():
    user_id = int(get_jwt_identity())
    
    new_account = Account(user_id=user_id, balance=0.00)
    db.session.add(new_account)
    db.session.commit()

    return jsonify({
        'message': 'Account created successfully',
        'account_id': new_account.id,
        'account_number': new_account.account_number,
        'balance': str(new_account.balance)
    }), 201

@accounts_bp.route('/', methods=['GET'])
@jwt_required()
def get_accounts():
    user_id = int(get_jwt_identity())
    accounts = Account.query.filter_by(user_id=user_id).all()
    
    return jsonify([{
        'account_id': acc.id,
        'account_number': acc.account_number,
        'balance': str(acc.balance),
        'created_at': acc.created_at.isoformat()
    } for acc in accounts]), 200

@accounts_bp.route('/<int:account_id>', methods=['GET'])
@jwt_required()
def get_account_details(account_id):
    user_id = int(get_jwt_identity())
    account = Account.query.filter_by(id=account_id, user_id=user_id).first()
    
    if not account:
        return jsonify({'error': 'Account not found or access denied'}), 404

    return jsonify({
        'account_id': account.id,
        'account_number': account.account_number,
        'balance': str(account.balance),
        'created_at': account.created_at.isoformat()
    }), 200
