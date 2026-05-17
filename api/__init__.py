from flask_restful import Api
from .user_api import UserResource
from .register_api import RegisterResource
from .login_api import LoginResource
from .transaction_api import TransactionResource
from .budget_api import BudgetResource
from .notification_api import NotificationResource
from .dashboard_api import DashboardResource

def register_apis(app):
    api = Api(app)

    api.add_resource(RegisterResource, '/api/register')
    api.add_resource(LoginResource, '/api/login')
    api.add_resource(UserResource, '/api/users', '/api/users/<int:user_id>')
    api.add_resource(TransactionResource, '/api/transactions', '/api/transactions/<int:transaction_id>')
    api.add_resource(BudgetResource, '/api/budgets', '/api/budgets/<int:id>')
    api.add_resource(NotificationResource, '/api/notifications', '/api/notifications/<int:id>')
    api.add_resource(DashboardResource, '/api/dashboard')