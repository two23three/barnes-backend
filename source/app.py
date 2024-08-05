from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_restful import Api
from models import db, User, Role, Income, IncomeCategory, Expense, ExpenseCategory, Debt, DebtPayment, FinancialReport, Transaction, Asset, SavingsGoal, Setting
from user import UserResource, UsersFinancialReport
from views import UserModelView, IncomeModelView, ExpenseModelView, DebtModelView, DebtPaymentModelView, TransactionModelView, AssetModelView, SavingsGoalModelView, SettingModelView
from income import IncomeResource, IncomeCategoryResource
from expense import ExpenseResource, ExpenseCategoryResource
from source.transaction import TransactionResource
import config
from assets import AssetResource 
from savingsGoal import SavingsGoalResource
from settings import SettingResource
app = Flask(__name__)
app.config.from_object(config.Config)

# Initialize extensions
db.init_app(app)
api = Api(app)
admin = Admin(app, name='MyApp', template_mode='bootstrap3')

# Add model views to Flask-Admin
admin.add_view(UserModelView(User, db.session))
admin.add_view(ModelView(Role, db.session))
admin.add_view(IncomeModelView(Income, db.session))
admin.add_view(ModelView(IncomeCategory, db.session))
admin.add_view(ExpenseModelView(Expense, db.session))
admin.add_view(ModelView(ExpenseCategory, db.session))
admin.add_view(DebtModelView(Debt, db.session))
admin.add_view(DebtPaymentModelView(DebtPayment, db.session))
admin.add_view(ModelView(FinancialReport, db.session))
admin.add_view(TransactionModelView(Transaction, db.session))
admin.add_view(AssetModelView(Asset, db.session))
admin.add_view(SavingsGoalModelView(SavingsGoal, db.session))
admin.add_view(SettingModelView(Setting, db.session))

# Add UserResource to the API
api.add_resource(UserResource, '/users', '/users/<int:id>')
api.add_resource(IncomeResource, '/incomes', '/incomes/<int:id>')
api.add_resource(IncomeCategoryResource, '/income_categories', '/income_categories/<int:id>')
api.add_resource(ExpenseResource, '/expenses', '/expenses/<int:id>')
api.add_resource(ExpenseCategoryResource, '/categories', '/categories/<int:id>')
api.add_resource(AssetResource, '/assets', '/assets/<int:id>')
api.add_resource(UsersFinancialReport, '/user/<int:user_id>/financialreports', '/user/<int:user_id>/financialreports/<int:report_id>')
api.add_resource(TransactionResource, '/transactions', '/transactions/<int:id>')
api.add_resource(SavingsGoalResource, '/savings', '/savings/<int:id>')
@app.route('/')
def index():
    return "Welcome to Barnes!"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
    app.run(debug=True)