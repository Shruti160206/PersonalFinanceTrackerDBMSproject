from flask_restful import Api
from .budget_api import BudgetResource
from .category_api import CategoryResource
from .login_api import LoginResource
from .register_api import RegisterResource
from .transaction_api import TransactionResource

def register_apis(app):
    api = Api(app)

    api.add_resource(RegisterResource, '/api/register')
    api.add_resource(LoginResource, '/api/login')
    api.add_resource(CategoryResource, '/api/categories')
    api.add_resource(TransactionResource, '/api/transactions', '/api/transactions/<int:transaction_id>')
    api.add_resource(BudgetResource, '/api/budgets', '/api/budgets/<int:budget_id>')