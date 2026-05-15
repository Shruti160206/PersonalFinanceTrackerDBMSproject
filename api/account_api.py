from flask_restful import Resource, request
from extensions import db
from models import Account

def serialize(obj):
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}

class AccountResource(Resource):

    def get(self, account_id=None):
        if account_id:
            return serialize(Account.query.get_or_404(account_id))
        return [serialize(a) for a in Account.query.all()]

    def post(self):
        acc = Account(**request.json)
        db.session.add(acc)
        db.session.commit()
        return {"message": "Account created"}, 201

    def put(self, account_id):
        acc = Account.query.get_or_404(account_id)
        for k, v in request.json.items():
            setattr(acc, k, v)
        db.session.commit()
        return {"message": "Account updated"}

    def delete(self, account_id):
        acc = Account.query.get_or_404(account_id)
        db.session.delete(acc)
        db.session.commit()
        return {"message": "Account deleted"}