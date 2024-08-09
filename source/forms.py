from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, PasswordField, DateField, BooleanField, TextAreaField, DecimalField
from wtforms.validators import DataRequired
from models import User, Role, Income, IncomeCategory, Expense, ExpenseCategory, Debt, DebtPayment, FinancialReport, Transaction,Asset, SavingsGoal, Setting
from decimal import Decimal

# Create a custom form for the User model
class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    phone_number = StringField('Phone Number')
    email = StringField('Email', validators=[DataRequired()])
    password_hash = PasswordField('Password', validators=[DataRequired()])
    role_id = SelectField('Role', coerce=int, validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        # Populate the role_id select field with options from the roles table
        self.role_id.choices = [(role.id, role.name) for role in Role.query.all()]

# Create a custom form for the Income model
class IncomeForm(FlaskForm):
    user_id = SelectField('User', coerce=int, validators=[DataRequired()])
    amount = StringField('Amount', validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    description = StringField('Description')
    is_recurring = BooleanField('Reccurring')
    category_id = SelectField('Category', coerce=int, validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(IncomeForm, self).__init__(*args, **kwargs)
        # Populate the user_id select field with options from the users table
        self.user_id.choices = [(user.id, user.name) for user in User.query.all()]
        # Populate the category_id select field with options from the income_categories table
        self.category_id.choices = [(category.id, category.name) for category in IncomeCategory.query.all()]

# Create a custom form for the Expense model
class ExpenseForm(FlaskForm):
    user_id = SelectField('User', coerce=int, validators=[DataRequired()])
    amount = StringField('Amount', validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    description = StringField('Description')
    is_recurring = BooleanField('Recurring')
    category_id = SelectField('Category', coerce=int, validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(ExpenseForm, self).__init__(*args, **kwargs)
        self.user_id.choices = [(user.id, user.name) for user in User.query.all()]
        self.category_id.choices = [(category.id, category.name) for category in ExpenseCategory.query.all()]

    def validate(self):
        # First, run the default validations
        if not super(ExpenseForm, self).validate():
            return False

        # Retrieve the selected category from the database
        category = ExpenseCategory.query.get(self.category_id.data)
        if not category:
            self.category_id.errors.append('Invalid category selected.')
            return False

        # Debugging: Check what values we're working with
        print(f"Category Limit: {category.limit}")
        print(f"Form Amount: {self.amount.data}")

        # Calculate total expenses in this category excluding the current expense
        existing_expenses = Expense.query.filter_by(category_id=self.category_id.data).all()
        total_expenses = sum(expense.amount for expense in existing_expenses)

        # Debugging: Print the total existing expenses
        print(f"Total Existing Expenses: {total_expenses}")

        # Add the new expense amount
        try:
            new_expense_amount = Decimal(self.amount.data)
            total_expenses += new_expense_amount
        except ValueError:
            self.amount.errors.append('Invalid amount format.')
            return False

        # Debugging: Check the total after adding the new expense
        print(f"Total Expenses After Adding New: {total_expenses}")

        # Check if the total exceeds the category limit
        if category.limit and total_expenses > category.limit:
            self.amount.errors.append(f'This expense would exceed the limit for {category.name}.')
            print(f"Validation Error: Total exceeds the limit.")
            return False

        return True

# Create a custom form for the Debt model
class DebtForm(FlaskForm):
    user_id = SelectField('User', coerce=int, validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    principal_amount = StringField('Amount', validators=[DataRequired()])
    interest_rate = StringField('Interest Rate')
    remaining_balance = StringField('Remaining Balance', validators=[DataRequired()])
    due_date = DateField('Due Date', format='%Y-%m-%d', validators=[DataRequired()])
    description = StringField('Description')

    def __init__(self, *args, **kwargs):
        super(DebtForm, self).__init__(*args, **kwargs)
        # Populate the user_id select field with options from the users table
        self.user_id.choices = [(user.id, user.name) for user in User.query.all()]
        # Populate the interest_rate field with a default value of 0
        self.interest_rate.data = '0'


# Create a custom form for the DebtPayment model
class DebtPaymentForm(FlaskForm):
    debt_id = SelectField('Debt', coerce=int, validators=[DataRequired()])
    amount = StringField('Amount', validators=[DataRequired()])
    payment_date = DateField('Payment Date', format='%Y-%m-%d', validators=[DataRequired()])
    description = StringField('Description')

    def __init__(self, *args, **kwargs):
        super(DebtPaymentForm, self).__init__(*args, **kwargs)
        # Populate the debt_id select field with options from the debts table
        self.debt_id.choices = [(debt.id, f'{debt.name} - {debt.principal_amount} ({debt.due_date})') for debt in Debt.query.all()]

# Create a custom form for the FinancialReport model
class FinancialReportForm(FlaskForm):
    user_id = SelectField('User', coerce=int, validators=[DataRequired()])
    report_type = StringField('Report Type', validators=[DataRequired()])
    report_data = TextAreaField('Report Data', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(FinancialReportForm, self).__init__(*args, **kwargs)
        # Populate the user_id select field with options from the users table
        self.user_id.choices = [(user.id, user.name) for user in User.query.all()]

# Create a custom form for the Transaction model
class TransactionForm(FlaskForm):
    user_id = SelectField('User', coerce=int, validators=[DataRequired()])
    amount = StringField('Amount', validators=[DataRequired()])  # Using DecimalField for monetary values
    transaction_type = StringField('Transaction Type', validators=[DataRequired()])
    category_id = SelectField('Category', coerce=int)  # Optional field
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    description = StringField('Description')

    def __init__(self, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        # Populate the user_id select field with options from the users table
        self.user_id.choices = [(user.id, user.name) for user in User.query.all()]
        # # Populate the category_id select field with options from the transaction_categories table
        # self.category_id.choices = [(category.id, category.name) for category in TransactionCategory.query.all()]

# Create a custom form for the Asset model
class AssetForm(FlaskForm):
    user_id = SelectField('User', coerce=int, validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    value = StringField('Value', validators=[DataRequired()])  # Using DecimalField for monetary values
    purchase_date = DateField('Purchase Date', format='%Y-%m-%d', validators=[DataRequired()])
    description = StringField('Description')

    def __init__(self, *args, **kwargs):
        super(AssetForm, self).__init__(*args, **kwargs)
        # Populate the user_id select field with options from the users table
        self.user_id.choices = [(user.id, user.name) for user in User.query.all()]

# Create a custom form for the SavingsGoal model
class SavingsGoalForm(FlaskForm):
    user_id = SelectField('User', coerce=int, validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    target_amount = StringField('Target Amount', validators=[DataRequired()])
    current_amount = StringField('Current Amount', validators=[DataRequired()])
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('End Date', format='%Y-%m-%d')  # Optional field
    description = StringField('Description')

    def __init__(self, *args, **kwargs):
        super(SavingsGoalForm, self).__init__(*args, **kwargs)
        # Populate the user_id select field with options from the users table
        self.user_id.choices = [(user.id, user.name) for user in User.query.all()]

# Create a custom form for the Setting model
class SettingForm(FlaskForm):
    user_id = SelectField('User', coerce=int, validators=[DataRequired()])
    setting_name = StringField('Setting Name', validators=[DataRequired()])
    setting_value = StringField('Setting Value', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(SettingForm, self).__init__(*args, **kwargs)
        # Populate the user_id select field with options from the users table
        self.user_id.choices = [(user.id, user.name) for user in User.query.all()]