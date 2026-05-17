from flask_restful import Api
from .user_api import UserResource
from .register_api import RegisterResource
from .login_api import LoginResource
from .account_api import AccountResource
from .transaction_api import TransactionResource
from .subscription_api import SubscriptionResource
from .budget_api import BudgetResource
from .loan_api import LoanResource
from .installment_api import InstallmentResource
from .notification_api import NotificationResource
from .dashboard_api import DashboardResource

def register_apis(app):
    api = Api(app)

    api.add_resource(RegisterResource, '/api/register')
    api.add_resource(LoginResource, '/api/login')
    api.add_resource(UserResource, '/api/users', '/api/users/<int:user_id>')
    api.add_resource(AccountResource, '/api/accounts', '/api/accounts/<int:account_id>')
    api.add_resource(TransactionResource, '/api/transactions', '/api/transactions/<int:transaction_id>')
    api.add_resource(SubscriptionResource, '/api/subscriptions', '/api/subscriptions/<int:id>')
    api.add_resource(BudgetResource, '/api/budgets', '/api/budgets/<int:id>')
    api.add_resource(LoanResource, '/api/loans', '/api/loans/<int:id>')
    api.add_resource(InstallmentResource, '/api/installments', '/api/installments/<int:id>')
    api.add_resource(NotificationResource, '/api/notifications', '/api/notifications/<int:id>')
    api.add_resource(DashboardResource, '/api/dashboard')