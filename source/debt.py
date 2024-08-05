from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from datetime import datetime
from models import db, Debt

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)
api = Api(app)

class DebtResource(Resource):
    def get(self, id=None):
        if id:
            debt = Debt.query.get_or_404(id)
            debt_data = {
                'id': debt.id,
                'user_id': debt.user_id,
                'name': debt.name,
                'principal_amount': str(debt.principal_amount),
                'interest_rate': str(debt.interest_rate),
                'remaining_balance': str(debt.remaining_balance),
                'due_date': debt.due_date.strftime('%Y-%m-%d'),
                'description': debt.description,
                'created_at': debt.created_at.isoformat(),
                'updated_at': debt.updated_at.isoformat()
            }
            return jsonify({'debt': debt_data})
        else:
            debts = Debt.query.all()
            output = []
            for debt in debts:
                debt_data = {
                    'id': debt.id,
                    'user_id': debt.user_id,
                    'name': debt.name,
                    'principal_amount': str(debt.principal_amount),
                    'interest_rate': str(debt.interest_rate),
                    'remaining_balance': str(debt.remaining_balance),
                    'due_date': debt.due_date.strftime('%Y-%m-%d'),
                    'description': debt.description,
                    'created_at': debt.created_at.isoformat(),
                    'updated_at': debt.updated_at.isoformat()
                }
                output.append(debt_data)
            return jsonify({'debts': output})

    def post(self):
        data = request.get_json()
        user_id = data.get('user_id')
        name = data.get('name')
        principal_amount = data.get('principal_amount')
        interest_rate = data.get('interest_rate')
        remaining_balance = data.get('remaining_balance')
        due_date = datetime.strptime(data.get('due_date'), '%Y-%m-%d').date()
        description = data.get('description')

        new_debt = Debt(user_id=user_id, name=name, principal_amount=principal_amount, 
                        interest_rate=interest_rate, remaining_balance=remaining_balance, 
                        due_date=due_date, description=description)
        db.session.add(new_debt)
        db.session.commit()

        return {'message': 'Debt created successfully'}, 201

    def put(self, id):
        data = request.get_json()
        debt = Debt.query.get_or_404(id)

        debt.user_id = data.get('user_id', debt.user_id)
        debt.name = data.get('name', debt.name)
        debt.principal_amount = data.get('principal_amount', debt.principal_amount)
        debt.interest_rate = data.get('interest_rate', debt.interest_rate)
        debt.remaining_balance = data.get('remaining_balance', debt.remaining_balance)
        debt.due_date = datetime.strptime(data.get('due_date', debt.due_date.strftime('%Y-%m-%d')), '%Y-%m-%d').date()
        debt.description = data.get('description', debt.description)

        db.session.commit()

        return {'message': 'Debt updated successfully'}

    def delete(self, id):
        debt = Debt.query.get_or_404(id)
        db.session.delete(debt)
        db.session.commit()

        return {'message': 'Debt deleted successfully'}

api.add_resource(DebtResource, '/debts', '/debts/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)