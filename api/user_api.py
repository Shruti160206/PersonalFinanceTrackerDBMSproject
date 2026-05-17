from flask_restful import Resource
from models import User

def serialize(obj):
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
class UserResource(Resource):

    def get(self, user_id=None):
        if user_id:
            return serialize(User.query.get_or_404(user_id))
        return [serialize(u) for u in User.query.all()]