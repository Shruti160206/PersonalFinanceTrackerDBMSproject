from flask_restful import Resource, request
from flask_login import current_user, login_required
from extensions import db
from models import Budget

def serialize(obj):
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}

class BudgetResource(Resource):
    
    @login_required
    def post(self):
        data = request.json

        category_id = data.get("category_id")
        limit_amount = data.get("limit_amount")
        month = data.get("month")
        year = data.get("year")

        # validation
        if not category_id or not limit_amount or not month or not year:
            return {"error": "All fields are required"}, 400

        # check if budget already exists
        existing_budget = Budget.query.filter_by(
            user_id=current_user.user_id,
            category_id=category_id,
            month=month,
            year=year
        ).first()

        if existing_budget:
            return {
                "error": "Budget already exists for this category, month and year"
            }, 409

        # create budget
        budget = Budget(
            user_id=current_user.user_id,
            category_id=category_id,
            limit_amount=limit_amount,
            month=month,
            year=year
        )

        db.session.add(budget)
        db.session.commit()

        return {
            "message": "Budget created successfully"
        }, 201
    
    @login_required
    def delete(self, budget_id):

        # find budget belonging to current user
        budget = Budget.query.filter_by(
            budget_id=budget_id,
            user_id=current_user.user_id
        ).first()

        # budget not found
        if not budget:
            return {
                "error": "Budget not found"
            }, 404

        # delete budget
        db.session.delete(budget)
        db.session.commit()

        return {
            "message": "Budget deleted successfully"
        }, 200