from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.db import db
from ..models.account import Account
from ..models.transaction import Transaction
from ..services.transaction_service import deposit, withdraw, transfer

transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('/deposit', methods=['POST'])
@jwt_required()
def make_deposit():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    
    account_id = data.get('account_id')
    amount = data.get('amount')
    
    if not account_id or amount is None:
        return jsonify({'error': 'account_id and amount are required'}), 400
        
    account = Account.query.filter_by(id=account_id, user_id=user_id).first()
    if not account:
        return jsonify({'error': 'Account not found or access denied'}), 404
        
    try:
        deposit(account, amount)
        db.session.commit()
        return jsonify({'message': 'Deposit successful', 'new_balance': str(account.balance)}), 200
    except ValueError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500

@transactions_bp.route('/withdraw', methods=['POST'])
@jwt_required()
def make_withdrawal():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    
    account_id = data.get('account_id')
    amount = data.get('amount')
    
    if not account_id or amount is None:
        return jsonify({'error': 'account_id and amount are required'}), 400
        
    account = Account.query.filter_by(id=account_id, user_id=user_id).first()
    if not account:
        return jsonify({'error': 'Account not found or access denied'}), 404
        
    try:
        withdraw(account, amount)
        db.session.commit()
        return jsonify({'message': 'Withdrawal successful', 'new_balance': str(account.balance)}), 200
    except ValueError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500

@transactions_bp.route('/transfer', methods=['POST'])
@jwt_required()
def make_transfer():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    
    from_account_id = data.get('from_account_id')
    to_account_number = data.get('to_account_number')
    amount = data.get('amount')
    
    if not from_account_id or not to_account_number or amount is None:
        return jsonify({'error': 'from_account_id, to_account_number, and amount are required'}), 400
        
    from_account = Account.query.filter_by(id=from_account_id, user_id=user_id).first()
    if not from_account:
        return jsonify({'error': 'Source account not found or access denied'}), 404
        
    to_account = Account.query.filter_by(account_number=to_account_number).first()
    if not to_account:
        return jsonify({'error': 'Destination account not found'}), 404
        
    if from_account.id == to_account.id:
        return jsonify({'error': 'Cannot transfer to the same account'}), 400
        
    try:
        transfer(from_account, to_account, amount)
        db.session.commit()
        return jsonify({'message': 'Transfer successful', 'new_balance': str(from_account.balance)}), 200
    except ValueError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500
        
@transactions_bp.route('/history/<int:account_id>', methods=['GET'])
@jwt_required()
def get_history(account_id):
    user_id = int(get_jwt_identity())
    
    account = Account.query.filter_by(id=account_id, user_id=user_id).first()
    if not account:
        return jsonify({'error': 'Account not found or access denied'}), 404
        
    transactions = Transaction.query.filter_by(account_id=account_id).order_by(Transaction.created_at.desc()).all()
    
    return jsonify([{
        'transaction_id': tx.id,
        'type': tx.transaction_type,
        'amount': str(tx.amount),
        'balance_after': str(tx.balance_after),
        'related_account_id': tx.related_account_id,
        'description': tx.description,
        'timestamp': tx.created_at.isoformat()
    } for tx in transactions]), 200
