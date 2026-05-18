from extensions import db
from datetime import datetime
from flask_login import UserMixin

# ---------------- USERS ---------------- #
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True, nullable=False)
    date_of_birth = db.Column(db.Date)
    password = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_id(self):
        return str(self.user_id)


# ---------------- TRANSACTION CATEGORY ---------------- #
class TransactionCategory(db.Model):
    __tablename__ = 'transactioncategories'

    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            "category_id": self.category_id,
            "category_name": self.category_name
        }


# ---------------- TRANSACTIONS ---------------- #
class Transaction(db.Model):
    __tablename__ = 'transactions'

    transaction_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    category_id = db.Column(db.Integer, db.ForeignKey('transactioncategories.category_id'))
    amount = db.Column(db.Float, nullable=False)
    transaction_date = db.Column(db.Date, default=datetime.utcnow)


# ---------------- BUDGETS ---------------- #
class Budget(db.Model):
    __tablename__ = 'budgets'

    budget_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    category_id = db.Column(db.Integer, db.ForeignKey('transactioncategories.category_id'))
    limit_amount = db.Column(db.Float)
    month = db.Column(db.Integer)
    year = db.Column(db.Integer)

# ---------------- NOTIFICATIONS ---------------- #
class Notification(db.Model):
    __tablename__ = 'notifications'

    notification_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    message = db.Column(db.String(255))
    notification_date = db.Column(db.Date, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)