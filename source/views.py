from flask_bcrypt import Bcrypt
from flask_admin.contrib.sqla import ModelView

from forms import UserForm, IncomeForm, ExpenseForm, DebtForm, DebtPaymentForm, TransactionForm, AssetForm, SavingsGoalForm, SettingForm

bcrypt = Bcrypt()  # Initialize Bcrypt

# Define a custom ModelView for the User model
class UserModelView(ModelView):
    form = UserForm
    form_excluded_columns = ('created_at', 'updated_at')

    def on_model_change(self, form, model, is_created):
        if is_created or form.password_hash.data:
            # Hash the password before saving it
            model.password_hash = bcrypt.generate_password_hash(form.password_hash.data).decode('utf-8')
        # Ensure that role_id is set to a default if it is None
        if model.role_id is None:
            model.role_id = 1  # Replace 1 with the ID of the default role if needed

# Define a custom ModelView for the Income model
class IncomeModelView(ModelView):
    form = IncomeForm
    form_excluded_columns = ('created_at', 'updated_at')

# Define a custom ModelView for the Expense model
class ExpenseModelView(ModelView):
    form = ExpenseForm
    form_excluded_columns = ('created_at', 'updated_at')

# Define a custom ModelView for the Debt model
class DebtModelView(ModelView):
    form = DebtForm
    form_excluded_columns = ('created_at', 'updated_at')

# Define a custom ModelView for the DebtPayment model
class DebtPaymentModelView(ModelView):
    form = DebtPaymentForm
    form_excluded_columns = ('created_at', 'updated_at')

# Define a custom ModelView for the Transaction model
class TransactionModelView(ModelView):
    form = TransactionForm
    form_excluded_columns = ('created_at', 'updated_at')

# Define a custom ModelView for the Asset model
class AssetModelView(ModelView):
    form = AssetForm
    form_excluded_columns = ('created_at', 'updated_at')

# Define a custom ModelView for the SavingsGoal model
class SavingsGoalModelView(ModelView):
    form = SavingsGoalForm
    form_excluded_columns = ('created_at', 'updated_at')

# Define a custom ModelView for the Setting model
class SettingModelView(ModelView):
    form = SettingForm
    form_excluded_columns = ('created_at', 'updated_at')