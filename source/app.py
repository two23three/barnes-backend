from flask import Flask, request, jsonify
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_restful import Api
from flask_cors import CORS  
from models import db, User, Role, Income, IncomeCategory, Expense, ExpenseCategory, Debt, DebtPayment, FinancialReport, Transaction, Asset, SavingsGoal, Setting
from user import UserResource, UsersFinancialReport
from views import UserModelView, IncomeModelView, ExpenseModelView, DebtModelView, DebtPaymentModelView, TransactionModelView, AssetModelView, SavingsGoalModelView, SettingModelView
from income import IncomeResource, IncomeCategoryResource
from expense import ExpenseResource, ExpenseCategoryResource
from assets import AssetResource 
from transaction import TransactionResource
from savingsGoal import SavingsGoalResource
from settings import SettingResource
from debt import DebtResource
from debtPayment import DebtPaymentResource
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

from flask_bcrypt import Bcrypt
import config
import re

app = Flask(__name__)
app.config.from_object(config.Config)

# Initialize extensions
db.init_app(app)
api = Api(app)
admin = Admin(app, name='MyApp', template_mode='bootstrap3')
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
CORS(app)  

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
api.add_resource(SettingResource, '/settings', '/settings/<int:id>')

# Define validation patterns
email_pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
kenyan_phone_pattern = re.compile(r"^(?:\+254|0)[71]\d{8}$")

@app.route('/')
def index():
    return "Welcome to BizzGogo!"

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    
    if not all(key in data for key in ('name', 'email', 'password', 'role_id')):
        return jsonify({'msg': 'Missing required fields'}), 400
    
    name = data.get('name')
    phone_number = data.get('phone_number')
    email = data.get('email')
    password = data.get('password')
    role_id = data.get('role_id')
    referral_code = data.get('referral_code')
    
    if User.query.filter_by(email=email).first():
        return jsonify({'msg': 'User already exists'}), 400
    
    if not email_pattern.match(email):
        return jsonify({'msg': 'Invalid email format'}), 400

    if phone_number and not kenyan_phone_pattern.match(phone_number):
        return jsonify({'msg': 'Invalid phone number format'}), 400
    
    # Check if referral code exists and is valid
    referred_by_user = None
    if referral_code:
        referred_by_user = User.query.filter_by(referral_code=referral_code).first()
        if not referred_by_user:
            return jsonify({'msg': 'Invalid referral code'}), 400
    
    # Generate a unique referral code for the new user
    new_user_referral_code = f"{name[:3]}-{str(uuid.uuid4())[:4]}"
    
    hashed_password = generate_password_hash(password)
    
    new_user = User(
        name=name,
        phone_number=phone_number,
        email=email,
        password_hash=hashed_password,
        role_id=role_id,
        referral_code=new_user_referral_code,
        referred_by=referred_by_user.referral_code if referred_by_user else None
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    access_token = create_access_token(identity=new_user.id)
    refresh_token = create_refresh_token(identity=new_user.id)
    
    return jsonify({
        'msg': 'User created successfully',
        'access_token': access_token,
        'refresh_token': refresh_token
    }), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not all(key in data for key in ('password',)):
        return jsonify({'msg': 'Missing required fields'}), 400

    email = data.get('email')
    phone_number = data.get('phone_number')
    password = data.get('password')
    
    if not email and not phone_number:
        return jsonify({'msg': 'Missing email or phone number'}), 400

    if email and not email_pattern.match(email):
        return jsonify({'msg': 'Invalid email format'}), 400

    if phone_number and not kenyan_phone_pattern.match(phone_number):
        return jsonify({'msg': 'Invalid phone number format'}), 400

    user = None
    if email:
        user = User.query.filter_by(email=email).first()
    if phone_number:
        user = User.query.filter_by(phone_number=phone_number).first()
    
    if not user or not check_password_hash(user.password_hash, password):
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
