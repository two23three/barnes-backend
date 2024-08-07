from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from datetime import datetime
from models import db, Expense, ExpenseCategory
from config import Config

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
                'amount': expense.amount,
                'category_id': expense.category_id,
                'date': expense.date,
                'description': expense.description,
                'created_at': expense.created_at,
                'updated_at': expense.updated_at
            }
            return jsonify({'expense': expense_data})
        else:
            expenses = Expense.query.all()
            output = []
            for expense in expenses:
                expense_data = {
                    'id': expense.id,
                    'user_id': expense.user_id,
                    'amount': expense.amount,
                    'category_id': expense.category_id,
                    'date': expense.date,
                    'description': expense.description,
                    'created_at': expense.created_at,
                    'updated_at': expense.updated_at
                }
                output.append(expense_data)
            return jsonify({'expenses': output})

    def post(self):
        data = request.get_json()
        user_id = data.get('user_id')
        amount = data.get('amount')
        category_id = data.get('category_id')
        date = datetime.strptime(data.get('date'), '%Y-%m-%d')
        description = data.get('description')

        new_expense = Expense(user_id=user_id, amount=amount, category_id=category_id, date=date, description=description)
        db.session.add(new_expense)
        db.session.commit()

        return {'message': 'Expense created successfully'}, 201

    def put(self, id):
        data = request.get_json()
        expense = Expense.query.get_or_404(id)

        expense.user_id = data.get('user_id', expense.user_id)
        expense.amount = data.get('amount', expense.amount)
        expense.category_id = data.get('category_id', expense.category_id)
        expense.date = datetime.strptime(data.get('date', expense.date.strftime('%Y-%m-%d')), '%Y-%m-%d')
        expense.description = data.get('description', expense.description)

        db.session.commit()

        return {'message': 'Expense updated successfully'}

    def delete(self, id):
        expense = Expense.query.get_or_404(id)
        db.session.delete(expense)
        db.session.commit()

        return {'message': 'Expense deleted successfully'}

class ExpenseCategoryResource(Resource):
    def get(self, id=None):
        if id:
            category = ExpenseCategory.query.get_or_404(id)
            category_data = {
                'id': category.id,
                'name': category.name,
                'description': category.description,
                'user_id': category.user_id
            }
            return jsonify({'category': category_data})
        else:
            categories = ExpenseCategory.query.all()
            output = []
            for category in categories:
                category_data = {
                    'id': category.id,
                    'name': category.name,
                    'description': category.description,
                    'user_id': category.user_id
                }
                output.append(category_data)
            return jsonify({'categories': output})

    def post(self):
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        user_id = data.get('user_id')

        new_category = ExpenseCategory(name=name, description=description, user_id=user_id)
        db.session.add(new_category)
        db.session.commit()

        return {'message': 'Category created successfully'}, 201

    def put(self, id):
        data = request.get_json()
        category = ExpenseCategory.query.get_or_404(id)

        category.name = data.get('name', category.name)
        category.description = data.get('description', category.description)
        category.user_id = data.get('user_id', category.user_id)

        db.session.commit()

        return {'message': 'Category updated successfully'}

    def delete(self, id):
        category = ExpenseCategory.query.get_or_404(id)
        db.session.delete(category)
        db.session.commit()

        return {'message': 'Category deleted successfully'}


if __name__ == '__main__':
    app.run(debug=True)