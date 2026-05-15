from flask_restful import Resource, request
from extensions import db
from models import User

def serialize(obj):
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}

class UserResource(Resource):

    def get(self, user_id=None):
        if user_id:
            return serialize(User.query.get_or_404(user_id))
        return [serialize(u) for u in User.query.all()]

    def post(self):
        user = User(**request.json)
        db.session.add(user)
        db.session.commit()
        return {"message": "User created"}, 201

    def put(self, user_id):
        user = User.query.get_or_404(user_id)
        for k, v in request.json.items():
            setattr(user, k, v)
        db.session.commit()
        return {"message": "User updated"}

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted"}