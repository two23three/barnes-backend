from flask import Flask
from flask import Flask, request, jsonify
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_restful import Api
from models import db, User, Role, Income, IncomeCategory, Expense, ExpenseCategory, Debt, DebtPayment, FinancialReport, Transaction, Asset, SavingsGoal, Setting
from user import UserResource, UsersFinancialReport
from views import UserModelView, IncomeModelView, ExpenseModelView, DebtModelView, DebtPaymentModelView, TransactionModelView, AssetModelView, SavingsGoalModelView, SettingModelView
from income import IncomeResource, IncomeCategoryResource
from expense import ExpenseResource, ExpenseCategoryResource
from source.transaction import TransactionResource
from debt import DebtResource
from debtPayment import DebtPaymentResource
import config
from assets import AssetResource 
from savingsGoal import SavingsGoalResource
from settings import SettingResource
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
app = Flask(__name__)
app.config.from_object(config.Config)

# Initialize extensions
db.init_app(app)
api = Api(app)
admin = Admin(app, name='MyApp', template_mode='bootstrap3')
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

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
api.add_resource(DebtResource, '/debts', '/debts/<int:id>')
api.add_resource(DebtPaymentResource, '/debt_payments', '/debt_payments/<int:id>')
api.add_resource(AssetResource, '/assets', '/assets/<int:id>')
api.add_resource(UsersFinancialReport, '/user/<int:user_id>/financialreports', '/user/<int:user_id>/financialreports/<int:report_id>')
api.add_resource(TransactionResource, '/transactions', '/transactions/<int:id>')
api.add_resource(SavingsGoalResource, '/savings', '/savings/<int:id>')
@app.route('/')
def index():
    return "Welcome to Barnes!"

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    # Validate input data
    if not all(key in data for key in ('name', 'email', 'password', 'role_id')):
        return jsonify({'msg': 'Missing required fields'}), 400

    name = data.get('name')
    phone_number = data.get('phone_number')
    email = data.get('email')
    password = data.get('password')
    role_id = data.get('role_id')

    # Check if user already exists
    if User.query.filter_by(email=email).first():
        return jsonify({'msg': 'User already exists'}), 400

    # Hash the password using Flask-Bcrypt
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Create a new user
    new_user = User(
        name=name,
        phone_number=phone_number,
        email=email,
        password_hash=hashed_password,
        role_id=role_id
    )

    db.session.add(new_user)
    db.session.commit()

    # Create access token
    access_token = create_access_token(identity=new_user.id)
    refresh_token = create_refresh_token(identity=new_user.id)

    return jsonify({
        'msg': 'User created successfully'
    }), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not all(key in data for key in ('email', 'password')):
        return jsonify({'msg': 'Missing required fields'}), 400

    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({'msg': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    return jsonify({
        'msg': 'Login successful',
        'access_token': access_token,
        'refresh_token': refresh_token
    }), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
    app.run(debug=True)