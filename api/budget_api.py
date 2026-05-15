from flask_restful import Resource, request
from extensions import db
from models import Budget

def serialize(obj):
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}

class BudgetResource(Resource):

    def get(self, id=None):
        if id:
            return serialize(Budget.query.get_or_404(id))
        return [serialize(b) for b in Budget.query.all()]

    def post(self):
        b = Budget(**request.json)
        db.session.add(b)
        db.session.commit()
        return {"message": "Budget created"}, 201

    def put(self, id):
        b = Budget.query.get_or_404(id)
        for k, v in request.json.items():
            setattr(b, k, v)
        db.session.commit()
        return {"message": "Budget updated"}

    def delete(self, id):
        b = Budget.query.get_or_404(id)
        db.session.delete(b)
        db.session.commit()
        return {"message": "Budget deleted"}