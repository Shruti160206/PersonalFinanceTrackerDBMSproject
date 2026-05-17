from flask_restful import Resource, request
from models import User
from extensions import bcrypt
from flask_login import login_user

class LoginResource(Resource):

    def post(self):
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        print(data)

        if not email or not password:
            return {"error": "All fields are required"}, 400

        # get user by email ONLY
        user = User.query.filter_by(email=email).first()

        if not user:
            return {"error": "Incorrect email or password"}, 401

        # compare password with stored hash
        if not bcrypt.check_password_hash(user.password, password):
            return {"error": "Incorrect email or password"}, 401

        login_user(user)
        return {"message": "Successfully logged in!"}, 200