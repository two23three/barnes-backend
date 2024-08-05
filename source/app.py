from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_restful import Api
from models import db, User, Role, Income, IncomeCategory, Expense, ExpenseCategory, Debt, DebtPayment, FinancialReport, Transaction, Asset, SavingsGoal, Setting
from user import UserResource
from expense import ExpenseResource, ExpenseCategoryResource
import config
app = Flask(__name__)
app.config.from_object(config.Config)
# Initialize extensions
db.init_app(app)
api = Api(app)
admin = Admin(app, name='MyApp', template_mode='bootstrap3')
# Add model views to Flask-Admin
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Role, db.session))
admin.add_view(ModelView(Income, db.session))
admin.add_view(ModelView(IncomeCategory, db.session))
admin.add_view(ModelView(Expense, db.session))
admin.add_view(ModelView(ExpenseCategory, db.session))
admin.add_view(ModelView(Debt, db.session))
admin.add_view(ModelView(DebtPayment, db.session))
admin.add_view(ModelView(FinancialReport, db.session))
admin.add_view(ModelView(Transaction, db.session))
admin.add_view(ModelView(Asset, db.session))
admin.add_view(ModelView(SavingsGoal, db.session))
admin.add_view(ModelView(Setting, db.session))
# Add UserResource to the API
api.add_resource(UserResource, '/users', '/users/<int:id>')
api.add_resource(ExpenseResource, '/expenses', '/expenses/<int:id>')
api.add_resource(ExpenseCategoryResource, '/categories', '/categories/<int:id>')
@app.route('/')
def index():
    return "Welcome to BizzGogo!"


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)