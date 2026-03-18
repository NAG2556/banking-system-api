from .db import db
from datetime import datetime, timezone

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False) # DEPOSIT, WITHDRAWAL, TRANSFER_IN, TRANSFER_OUT
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    balance_after = db.Column(db.Numeric(10, 2), nullable=False)
    related_account_id = db.Column(db.Integer, nullable=True) # For transfers
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
