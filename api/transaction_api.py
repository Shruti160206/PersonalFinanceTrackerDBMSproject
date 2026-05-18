from flask_restful import Resource, request
from flask_login import current_user, login_required
from extensions import db
from models import Transaction
from datetime import date, datetime

def serialize(obj):
    result = {}
    for c in obj.__table__.columns:
        value = getattr(obj, c.name)
        if isinstance(value, (date, datetime)):
            value = value.isoformat()
        result[c.name] = value
    return result

class TransactionResource(Resource):

    @login_required
    def post(self):
        data = request.json

        t = Transaction(
            user_id=current_user.user_id,
            amount=data.get("amount"),
            category_id=data.get("category_id"),
            transaction_date=data.get("transaction_date")
        )

        db.session.add(t)
        db.session.commit()

        return {
            "message": "Transaction created",
            "transaction": serialize(t)
        }, 201
    
    @login_required
    def delete(self, transaction_id):
        transaction = Transaction.query.filter_by(
            transaction_id=transaction_id,
            user_id=current_user.user_id
        ).first()

        if not transaction:
            return {"error": "Transaction not found"}, 404

        db.session.delete(transaction)
        db.session.commit()

        return {"message": "Transaction deleted successfully"}, 200