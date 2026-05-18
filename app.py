from flask import Flask, render_template, request
from config import Config
from extensions import db, bcrypt, migrate, login_manager
from api import register_apis
from models import User
from flask_login import logout_user, login_required, current_user
from models import Transaction, TransactionCategory, Notification, Budget
from sqlalchemy import extract, func

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
bcrypt.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)

login_manager.login_view = 'login'

# Register APIs
register_apis(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    result = db.session.execute(
        db.text("CALL GetDashboardSummary(:user_id)"),
        {"user_id": current_user.user_id}
    )
    row = result.fetchone()

    recent_transactions = (
    db.session.query(
            Transaction.transaction_id,
            Transaction.amount,
            Transaction.transaction_date,
            Transaction.user_id,
            Transaction.category_id,
            TransactionCategory.category_name
        )
        .join(TransactionCategory, Transaction.category_id == TransactionCategory.category_id)
        .filter(Transaction.user_id == current_user.user_id)
        .order_by(Transaction.transaction_date.desc(), Transaction.transaction_id.desc())
        .limit(5)
        .all()
    )
    
    return render_template(
        "dashboard.html",
        monthly_expense=row.monthly_expense,
        monthly_notification_count=row.monthly_notification_count,
        recent_transactions=recent_transactions
    )

@app.route('/transactions')
@login_required
def transactions():
    categories = TransactionCategory.query.all()

    category_id = request.args.get("category_id")

    query = db.session.query(
        Transaction.transaction_id,
        Transaction.amount,
        Transaction.transaction_date,
        Transaction.user_id,
        Transaction.category_id,
        TransactionCategory.category_name
    ).join(
        TransactionCategory,
        Transaction.category_id == TransactionCategory.category_id
    ).order_by(Transaction.transaction_date.desc(), Transaction.transaction_id.desc()
    ).filter(
        Transaction.user_id == current_user.user_id
    )

    # filter based on category id if it exists
    if category_id:
        query = query.filter(Transaction.category_id == category_id)

    transactions = query.all()

    return render_template(
        "transactions.html",
        transactions=transactions,
        categories=categories
    )

@app.route('/budgets')
@login_required
def budgets():
    categories = TransactionCategory.query.all()

    budgets = db.session.query(
        Budget.budget_id,
        Budget.category_id,
        Budget.limit_amount,
        Budget.month,
        Budget.year,

        TransactionCategory.category_name,

        # total spent for that category/month/year
        func.coalesce(func.sum(Transaction.amount), 0).label("spent")

    ).join(
        TransactionCategory,
        Budget.category_id == TransactionCategory.category_id

    ).outerjoin(
        Transaction,
        (Transaction.category_id == Budget.category_id) &
        (Transaction.user_id == Budget.user_id) &
        (extract('month', Transaction.transaction_date) == Budget.month) &
        (extract('year', Transaction.transaction_date) == Budget.year)

    ).filter(
        Budget.user_id == current_user.user_id

    ).group_by(
        Budget.budget_id,
        Budget.category_id,
        Budget.limit_amount,
        Budget.month,
        Budget.year,
        TransactionCategory.category_name

    ).all()

    return render_template(
        "budgets.html",
        budgets=budgets,
        categories=categories
    )

@app.route('/notifications')
@login_required
def notifications():

    notifications = Notification.query.filter_by(
        user_id=current_user.user_id
    ).order_by(Notification.notification_date.desc()).all()

    # 👉 create snapshot with ordering (unread first)
    notifications_to_display = [
        {
            "notification_id": n.notification_id,
            "message": n.message,
            "notification_date": n.notification_date,
            "is_read": n.is_read
        }
        for n in notifications
    ]

    # sort: unread (False) first, then read (True)
    notifications_to_display.sort(key=lambda x: x["is_read"])

    # now mark as read (after snapshot)
    for n in notifications:
        n.is_read = True

    db.session.commit()

    return render_template(
        "notifications.html",
        notifications=notifications_to_display
    )

@app.route('/logout')
def logout():
    logout_user()
    return render_template('login.html')

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(debug=True)