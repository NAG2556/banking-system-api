from .db import db
from datetime import datetime, timezone
import random
import string

def generate_account_number():
    return ''.join(random.choices(string.digits, k=10))

class Account(db.Model):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    account_number = db.Column(db.String(20), unique=True, nullable=False, default=generate_account_number)
    balance = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    transactions = db.relationship('Transaction', backref='account', lazy=True)
