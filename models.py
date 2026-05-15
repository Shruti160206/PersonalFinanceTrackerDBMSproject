from extensions import db
from datetime import datetime

# ---------------- USERS ---------------- #
class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True, nullable=False)
    date_of_birth = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ---------------- ACCOUNTS ---------------- #
class Account(db.Model):
    __tablename__ = 'accounts'

    account_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    account_type = db.Column(db.String(20))
    balance = db.Column(db.Float, default=0)


# ---------------- TRANSACTION CATEGORY ---------------- #
class TransactionCategory(db.Model):
    __tablename__ = 'transaction_categories'

    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(50), nullable=False)


# ---------------- TRANSACTIONS ---------------- #
class Transaction(db.Model):
    __tablename__ = 'transactions'

    transaction_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.account_id'))
    category_id = db.Column(db.Integer, db.ForeignKey('transaction_categories.category_id'))
    amount = db.Column(db.Float, nullable=False)
    transaction_type = db.Column(db.String(10))  # income/expense
    transaction_date = db.Column(db.Date, default=datetime.utcnow)


# ---------------- SUBSCRIPTIONS ---------------- #
class Subscription(db.Model):
    __tablename__ = 'subscriptions'

    subscription_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    service_name = db.Column(db.String(50))
    monthly_fee = db.Column(db.Float)
    start_date = db.Column(db.Date)
    next_due_date = db.Column(db.Date)
    status = db.Column(db.String(20))


# ---------------- BUDGETS ---------------- #
class Budget(db.Model):
    __tablename__ = 'budgets'

    budget_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    category_id = db.Column(db.Integer, db.ForeignKey('transaction_categories.transaction_id'))
    limit_amount = db.Column(db.Float)
    month = db.Column(db.Integer)
    year = db.Column(db.Integer)


# ---------------- LOANS ---------------- #
class Loan(db.Model):
    __tablename__ = 'loans'

    loan_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    loan_type = db.Column(db.String(50))
    loan_amount = db.Column(db.Float)
    interest_rate = db.Column(db.Float)
    start_date = db.Column(db.Date)


# ---------------- INSTALLMENTS ---------------- #
class Installment(db.Model):
    __tablename__ = 'installments'

    installment_id = db.Column(db.Integer, primary_key=True)
    loan_id = db.Column(db.Integer, db.ForeignKey('loans.loan_id'))
    amount = db.Column(db.Float)
    due_date = db.Column(db.Date)
    status = db.Column(db.String(20))


# ---------------- NOTIFICATIONS ---------------- #
class Notification(db.Model):
    __tablename__ = 'notifications'

    notification_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    message = db.Column(db.String(255))
    notification_date = db.Column(db.Date, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)