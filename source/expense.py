from flask import Flask, request
from flask_restful import Resource, Api
from datetime import datetime
from models import db, Expense, ExpenseCategory
from config import Config
from decimal import Decimal, InvalidOperation
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
api = Api(app)

class ExpenseResource(Resource):
    def get(self, id=None):
        if id:
            expense = Expense.query.get_or_404(id)
            expense_data = {
                'id': expense.id,
                'user_id': expense.user_id,
                'amount': str(expense.amount),
                'category_id': expense.category_id,
                'date': expense.date.strftime('%Y-%m-%d'),
                'description': expense.description,
                'is_recurring': expense.is_recurring,
                'created_at': expense.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': expense.updated_at.strftime('%Y-%m-%d %H:%M:%S')
            }
            return {'expense': expense_data}
        else:
            expenses = Expense.query.all()
            output = []
            for expense in expenses:
                expense_data = {
                    'id': expense.id,
                    'user_id': expense.user_id,
                    'amount': str(expense.amount),
                    'category_id': expense.category_id,
                    'date': expense.date.strftime('%Y-%m-%d'),
                    'description': expense.description,
                    'is_recurring': expense.is_recurring,
                    'created_at': expense.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'updated_at': expense.updated_at.strftime('%Y-%m-%d %H:%M:%S')
                }
                output.append(expense_data)
            return {'expenses': output}

    def delete(self, id):
        expense = Expense.query.get_or_404(id)
        category = ExpenseCategory.query.get_or_404(expense.category_id)
        
        total_expenses = sum(Decimal(e.amount) for e in Expense.query.filter_by(category_id=category.id).all() if e.id != id)
        
        if category.limit and total_expenses > Decimal(category.limit):
            return {'message': 'Cannot delete expense: category limit would be exceeded'}, 400
        
        db.session.delete(expense)
        db.session.commit()

        return {'message': 'Expense deleted successfully'}
    
    def post(self):
        try:
            data = request.get_json()
            user_id = data.get('user_id')
            amount = Decimal(data.get('amount'))
            category_id = data.get('category_id')
            date = datetime.strptime(data.get('date'), '%Y-%m-%d')
            description = data.get('description')

            category = ExpenseCategory.query.get_or_404(category_id)

            total_expenses = sum(Decimal(expense.amount) for expense in Expense.query.filter_by(category_id=category_id).all()) + amount
            
            if category.limit and total_expenses > Decimal(category.limit):
                return {'message': 'Cannot add expense: category limit exceeded'}, 400

            new_expense = Expense(
                user_id=user_id, 
                amount=amount, 
                category_id=category_id, 
                date=date, 
                description=description
            )
            db.session.add(new_expense)
            db.session.commit()

            return {'message': 'Expense created successfully'}, 201
        except InvalidOperation:
            return {'message': 'Invalid amount value'}, 400
        except Exception as e:
            return {'message': f'An error occurred: {str(e)}'}, 500

    def put(self, id):
        try:
            data = request.get_json()
            expense = Expense.query.get_or_404(id)
            category = ExpenseCategory.query.get_or_404(expense.category_id)

            new_amount = Decimal(data.get('amount', expense.amount))
            
            total_expenses = sum(Decimal(e.amount) for e in Expense.query.filter_by(category_id=category.id).all() if e.id != id) + new_amount
            
            if category.limit and total_expenses > Decimal(category.limit):
                return {'message': 'Cannot update expense: category limit exceeded'}, 400

            expense.user_id = data.get('user_id', expense.user_id)
            expense.amount = new_amount
            expense.category_id = data.get('category_id', expense.category_id)
            expense.date = datetime.strptime(data.get('date', expense.date.strftime('%Y-%m-%d')), '%Y-%m-%d')
            expense.description = data.get('description', expense.description)

            db.session.commit()

            return {'message': 'Expense updated successfully'}
        except InvalidOperation:
            return {'message': 'Invalid amount value'}, 400
        except Exception as e:
            return {'message': f'An error occurred: {str(e)}'}, 500


class ExpenseCategoryResource(Resource):
    def get(self, id=None):
        if id:
            category = ExpenseCategory.query.get_or_404(id)
            category_data = {
                'id': category.id,
                'name': category.name,
                'description': category.description,
                'user_id': category.user_id,
                'limit': str(category.limit)  
            }
            return {'category': category_data}
        else:
            categories = ExpenseCategory.query.all()
            output = []
            for category in categories:
                category_data = {
                    'id': category.id,
                    'name': category.name,
                    'description': category.description,
                    'user_id': category.user_id,
                    'limit': str(category.limit)  
                }
                output.append(category_data)
            return {'categories': output}

    def post(self):
        try:
            data = request.get_json()

            # Extract and validate input data
            name = data.get('name')
            description = data.get('description')
            user_id = data.get('user_id')
            limit_str = data.get('limit')  # Optional limit field

            # Check for missing required fields
            if not name or not user_id:
                return {'message': 'Name and user_id are required fields.'}, 400

            # Validate and convert limit to Decimal if provided
            try:
                limit = Decimal(limit_str) if limit_str else None
            except (InvalidOperation, ValueError):
                return {'message': 'Invalid limit value.'}, 400

            # Create new category
            new_category = ExpenseCategory(
                name=name, 
                description=description, 
                user_id=user_id, 
                limit=limit
            )

            try:
                db.session.add(new_category)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                return {'message': 'Failed to create category. Integrity constraint violated.'}, 400
            except Exception as e:
                db.session.rollback()
                return {'message': f'An unexpected error occurred: {str(e)}'}, 500

            return {'message': 'Category created successfully'}, 201
        except Exception as e:
            return {'message': f'An error occurred: {str(e)}'}, 500
    
    def put(self, id):
        try:
            data = request.get_json()
            category = ExpenseCategory.query.get_or_404(id)

            category.name = data.get('name', category.name)
            category.description = data.get('description', category.description)
            category.user_id = data.get('user_id', category.user_id)
            
            limit_str = data.get('limit')
            if limit_str is not None:
                try:
                    category.limit = Decimal(limit_str)
                except (InvalidOperation, ValueError):
                    return {'message': 'Invalid limit value'}, 400

            db.session.commit()

            return {'message': 'Category updated successfully'}
        except Exception as e:
            return {'message': f'An error occurred: {str(e)}'}, 500

    def delete(self, id):
        try:
            category = ExpenseCategory.query.get_or_404(id)
            db.session.delete(category)
            db.session.commit()

            return {'message': 'Category deleted successfully'}
        except Exception as e:
            return {'message': f'An error occurred: {str(e)}'}, 500



if __name__ == '__main__':
    app.run(debug=True)
