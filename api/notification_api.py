from flask_restful import Resource, request
from extensions import db
from models import Notification

def serialize(obj):
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}

class NotificationResource(Resource):

    def get(self, id=None):
        if id:
            return serialize(Notification.query.get_or_404(id))
        return [serialize(n) for n in Notification.query.all()]

    def post(self):
        n = Notification(**request.json)
        db.session.add(n)
        db.session.commit()
        return {"message": "Notification created"}, 201

    def put(self, id):
        n = Notification.query.get_or_404(id)
        for k, v in request.json.items():
            setattr(n, k, v)
        db.session.commit()
        return {"message": "Notification updated"}

    def delete(self, id):
        n = Notification.query.get_or_404(id)
        db.session.delete(n)
        db.session.commit()
        return {"message": "Notification deleted"}