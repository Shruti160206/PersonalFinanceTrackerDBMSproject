from flask_restful import Resource, request
from extensions import db
from models import Loan

def serialize(obj):
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}

class LoanResource(Resource):

    def get(self, id=None):
        if id:
            return serialize(Loan.query.get_or_404(id))
        return [serialize(l) for l in Loan.query.all()]

    def post(self):
        l = Loan(**request.json)
        db.session.add(l)
        db.session.commit()
        return {"message": "Loan created"}, 201

    def put(self, id):
        l = Loan.query.get_or_404(id)
        for k, v in request.json.items():
            setattr(l, k, v)
        db.session.commit()
        return {"message": "Loan updated"}

    def delete(self, id):
        l = Loan.query.get_or_404(id)
        db.session.delete(l)
        db.session.commit()
        return {"message": "Loan deleted"}