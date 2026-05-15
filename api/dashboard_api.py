from flask_restful import Resource
from sqlalchemy import func
from datetime import datetime

from extensions import db
from models import (
    Account,
    Transaction,
    Subscription,
    Installment,
    Notification
)

class DashboardResource(Resource):

    def get(self):

       
        user_id = 1

        total_balance = db.session.query(
            func.sum(Account.balance)
        ).filter_by(user_id=user_id).scalar() or 0

        account_count = Account.query.filter_by(
            user_id=user_id
        ).count()

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

        active_subs = Subscription.query.filter_by(
            user_id=user_id,
            status='active'
        ).count()

        sub_monthly_total = db.session.query(
            func.sum(Subscription.monthly_fee)
        ).filter_by(
            user_id=user_id,
            status='active'
        ).scalar() or 0

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

        upcoming_subs = [
            {
                "service_name": s.service_name,
                "next_due_date": str(s.next_due_date)
            }
            for s in Subscription.query.filter_by(
                user_id=user_id
            ).limit(5)
        ]

        pending_installments = [
            {
                "id": i.installment_id,
                "amount": i.amount,
                "status": i.status
            }
            for i in Installment.query.filter_by(
                status='pending'
            ).limit(5)
        ]

        return {
            "now": str(datetime.now()),
            "total_balance": total_balance,
            "account_count": account_count,
            "monthly_income": monthly_income,
            "monthly_expense": monthly_expense,
            "income_tx_count": income_tx_count,
            "expense_tx_count": expense_tx_count,
            "active_subs": active_subs,
            "sub_monthly_total": sub_monthly_total,
            "recent_transactions": recent_transactions,
            "upcoming_subs": upcoming_subs,
            "pending_installments": pending_installments,
            "unread_count": unread_count
        }