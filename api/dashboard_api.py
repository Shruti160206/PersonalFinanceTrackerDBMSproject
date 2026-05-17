from flask_restful import Resource
from sqlalchemy import func
from datetime import datetime

from extensions import db
from models import (
    Transaction,
    Notification
)

class DashboardResource(Resource):

    def get(self):
        user_id = 1

        monthly_income = db.session.query(
            func.sum(Transaction.amount)
        ).filter_by(
            user_id=user_id,
            transaction_type='income'
        ).scalar() or 0

        monthly_expense = db.session.query(
            func.sum(Transaction.amount)
        ).filter_by(
            user_id=user_id,
            transaction_type='expense'
        ).scalar() or 0

        income_tx_count = Transaction.query.filter_by(
            user_id=user_id,
            transaction_type='income'
        ).count()

        expense_tx_count = Transaction.query.filter_by(
            user_id=user_id,
            transaction_type='expense'
        ).count()

        unread_count = Notification.query.filter_by(
            user_id=user_id,
            is_read=False
        ).count()

        recent_transactions = [
            {
                "id": t.transaction_id,
                "amount": t.amount,
                "transaction_type": t.transaction_type
            }
            for t in Transaction.query.filter_by(
                user_id=user_id
            ).limit(5)
        ]

        return {
            "now": str(datetime.now()),
            "monthly_income": monthly_income,
            "monthly_expense": monthly_expense,
            "income_tx_count": income_tx_count,
            "expense_tx_count": expense_tx_count,
            "recent_transactions": recent_transactions,
            "unread_count": unread_count
        }