from flask_restful import Resource, request
from extensions import db
from models import Subscription

def serialize(obj):
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}

class SubscriptionResource(Resource):

    def get(self, id=None):
        if id:
            return serialize(Subscription.query.get_or_404(id))
        return [serialize(s) for s in Subscription.query.all()]

    def post(self):
        s = Subscription(**request.json)
        db.session.add(s)
        db.session.commit()
        return {"message": "Subscription created"}, 201

    def put(self, id):
        s = Subscription.query.get_or_404(id)
        for k, v in request.json.items():
            setattr(s, k, v)
        db.session.commit()
        return {"message": "Subscription updated"}

    def delete(self, id):
        s = Subscription.query.get_or_404(id)
        db.session.delete(s)
        db.session.commit()
        return {"message": "Subscription deleted"}