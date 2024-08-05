from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from models import db, Income, IncomeCategory

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:newpassword@localhost/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
api = Api(app)

class IncomeResource(Resource):
    def get(self, id=None):
        if id:
            income = Income.query.get_or_404(id)
            income_data = {
                'id': income.id,
                'user_id': income.user_id,
                'amount': str(income.amount),
                'category_id': income.category_id,
                'date': income.date.strftime('%Y-%m-%d'),
                'description': income.description,
                'is_recurring': income.is_recurring,
                'created_at': income.created_at,
                'updated_at': income.updated_at
            }
            return jsonify({'income': income_data})
        else:
            incomes = Income.query.all()
            output = []
            for income in incomes:
                income_data = {
                    'id': income.id,
                    'user_id': income.user_id,
                    'amount': str(income.amount),
                    'category_id': income.category_id,
                    'date': income.date.strftime('%Y-%m-%d'),
                    'description': income.description,
                    'is_recurring': income.is_recurring,
                    'created_at': income.created_at,
                    'updated_at': income.updated_at
                }
                output.append(income_data)
            return jsonify({'incomes': output})

    def post(self):
        data = request.get_json()
        new_income = Income(
            user_id=data.get('user_id'),
            amount=data.get('amount'),
            category_id=data.get('category_id'),
            date=data.get('date'),
            description=data.get('description'),
            is_recurring=data.get('is_recurring', False)
        )
        db.session.add(new_income)
        db.session.commit()
        return {'message': 'Income added successfully'}, 201

    def put(self, id):
        data = request.get_json()
        income = Income.query.get_or_404(id)

        income.user_id = data.get('user_id', income.user_id)
        income.amount = data.get('amount', income.amount)
        income.category_id = data.get('category_id', income.category_id)
        income.date = data.get('date', income.date)
        income.description = data.get('description', income.description)
        income.is_recurring = data.get('is_recurring', income.is_recurring)

        db.session.commit()
        return {'message': 'Income updated successfully'}

    def delete(self, id):
        income = Income.query.get_or_404(id)
        db.session.delete(income)
        db.session.commit()
        return {'message': 'Income deleted successfully'}

class IncomeCategoryResource(Resource):
    def get(self, id=None):
        if id:
            category = IncomeCategory.query.get_or_404(id)
            category_data = {
                'id': category.id,
                'name': category.name,
                'description': category.description,
                'user_id': category.user_id
            }
            return jsonify({'income_category': category_data})
        else:
            categories = IncomeCategory.query.all()
            output = []
            for category in categories:
                category_data = {
                    'id': category.id,
                    'name': category.name,
                    'description': category.description,
                    'user_id': category.user_id
                }
                output.append(category_data)
            return jsonify({'income_categories': output})

    def post(self):
        data = request.get_json()
        new_category = IncomeCategory(
            name=data.get('name'),
            description=data.get('description'),
            user_id=data.get('user_id')
        )
        db.session.add(new_category)
        db.session.commit()
        return {'message': 'Income category added successfully'}, 201

    def put(self, id):
        data = request.get_json()
        category = IncomeCategory.query.get_or_404(id)

        category.name = data.get('name', category.name)
        category.description = data.get('description', category.description)
        category.user_id = data.get('user_id', category.user_id)

        db.session.commit()
        return {'message': 'Income category updated successfully'}

    def delete(self, id):
        category = IncomeCategory.query.get_or_404(id)
        db.session.delete(category)
        db.session.commit()
        return {'message': 'Income category deleted successfully'}

api.add_resource(IncomeResource, '/incomes', '/incomes/<int:id>')
api.add_resource(IncomeCategoryResource, '/income_categories', '/income_categories/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)