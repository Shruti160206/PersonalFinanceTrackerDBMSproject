from flask_restful import Resource, request
from extensions import db
from models import Transaction

def serialize(obj):
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}

class TransactionResource(Resource):

    def get(self, transaction_id=None):
        if transaction_id:
            return serialize(Transaction.query.get_or_404(transaction_id))
        return [serialize(t) for t in Transaction.query.all()]

    def post(self):
        t = Transaction(**request.json)
        db.session.add(t)
        db.session.commit()
        return {"message": "Transaction created"}, 201

    def put(self, transaction_id):
        t = Transaction.query.get_or_404(transaction_id)
        for k, v in request.json.items():
            setattr(t, k, v)
        db.session.commit()
        return {"message": "Transaction updated"}

    def delete(self, transaction_id):
        t = Transaction.query.get_or_404(transaction_id)
        db.session.delete(t)
        db.session.commit()
        return {"message": "Transaction deleted"}