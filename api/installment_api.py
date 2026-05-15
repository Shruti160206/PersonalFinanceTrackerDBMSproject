from flask_restful import Resource, request
from extensions import db
from models import Installment

def serialize(obj):
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}

class InstallmentResource(Resource):

    def get(self, id=None):
        if id:
            return serialize(Installment.query.get_or_404(id))
        return [serialize(i) for i in Installment.query.all()]

    def post(self):
        i = Installment(**request.json)
        db.session.add(i)
        db.session.commit()
        return {"message": "Installment created"}, 201

    def put(self, id):
        i = Installment.query.get_or_404(id)
        for k, v in request.json.items():
            setattr(i, k, v)
        db.session.commit()
        return {"message": "Installment updated"}

    def delete(self, id):
        i = Installment.query.get_or_404(id)
        db.session.delete(i)
        db.session.commit()
        return {"message": "Installment deleted"}