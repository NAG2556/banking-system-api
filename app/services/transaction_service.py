from ..models.db import db
from ..models.account import Account
from ..models.transaction import Transaction
from sqlalchemy.exc import IntegrityError
from decimal import Decimal

def deposit(account, amount, description="Deposit"):
    amount_decimal = Decimal(str(amount))
    if amount_decimal <= 0:
        raise ValueError("Deposit amount must be greater than zero")
    
    account.balance += amount_decimal
    
    tx = Transaction(
        account_id=account.id,
        transaction_type='DEPOSIT',
        amount=amount_decimal,
        balance_after=account.balance,
        description=description
    )
    
    db.session.add(tx)
    return tx

def withdraw(account, amount, description="Withdrawal"):
    amount_decimal = Decimal(str(amount))
    if amount_decimal <= 0:
        raise ValueError("Withdrawal amount must be greater than zero")
    
    if account.balance < amount_decimal:
        raise ValueError("Insufficient funds")
    
    account.balance -= amount_decimal
    
    tx = Transaction(
        account_id=account.id,
        transaction_type='WITHDRAWAL',
        amount=amount_decimal,
        balance_after=account.balance,
        description=description
    )
    
    db.session.add(tx)
    return tx

def transfer(from_account, to_account, amount, description="Transfer"):
    amount_decimal = Decimal(str(amount))
    if amount_decimal <= 0:
        raise ValueError("Transfer amount must be greater than zero")
        
    if from_account.balance < amount_decimal:
        raise ValueError("Insufficient funds")
        
    from_account.balance -= amount_decimal
    to_account.balance += amount_decimal
    
    tx_out = Transaction(
        account_id=from_account.id,
        transaction_type='TRANSFER_OUT',
        amount=amount_decimal,
        balance_after=from_account.balance,
        related_account_id=to_account.id,
        description=description
    )
    
    tx_in = Transaction(
        account_id=to_account.id,
        transaction_type='TRANSFER_IN',
        amount=amount_decimal,
        balance_after=to_account.balance,
        related_account_id=from_account.id,
        description=description
    )
    
    db.session.add(tx_out)
    db.session.add(tx_in)
    
    return tx_out
