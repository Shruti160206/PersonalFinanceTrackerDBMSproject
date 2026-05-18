from flask_restful import Resource
from models import TransactionCategory


class CategoryResource(Resource):

    def get(self, category_id=None):
        if category_id:
            category = TransactionCategory.query.get_or_404(category_id)
            return category.to_dict(), 200
        
        categories = TransactionCategory.query.all()

        return [c.to_dict() for c in categories], 200