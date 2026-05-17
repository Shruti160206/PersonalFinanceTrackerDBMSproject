from flask_restful import Resource, request
from extensions import db
from models import User
from extensions import bcrypt
from datetime import datetime

class RegisterResource(Resource):

    def post(self):
        data = request.get_json()
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        date_of_birth = data.get("date_of_birth")
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        if first_name == None or last_name == None or email == None or password == None or confirm_password == None:
            return {"error": "All fields are required"}, 400

        # check password match
        if password != confirm_password:
            return {"error": "Passwords do not match"}, 400

        # check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return {"error": "User with this email already exists"}, 409

        # convert date string → Python date object
        dob = None
        if date_of_birth:
            dob = datetime.strptime(date_of_birth, "%Y-%m-%d").date()

        # hash password
        password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

        print("register: " + password_hash)

        # user model creation
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            date_of_birth=dob,
            password=password_hash
        )

        db.session.add(user)
        db.session.commit()

        return {"message": "User created"}, 201