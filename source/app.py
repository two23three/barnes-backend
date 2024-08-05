# app.py

from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import db, User
import config
from models import db, User, Role, Income, IncomeCategory, Expense, ExpenseCategory, Debt, DebtPayment, FinancialReport, Transaction, Asset, SavingsGoal, Setting

app = Flask(__name__)
app.config.from_object(config.Config)

# Initialize extensions
db.init_app(app)
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

@app.route('/')
def index():
    return "Welcome to BizzGogo!"

if __name__ == '__main__':
    app.run(debug=True)