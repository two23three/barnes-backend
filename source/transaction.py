from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from models import db, Transaction

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:newpassword@localhost/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
api = Api(app)

class TransactionResource(Resource):
    def get(self, id=None):
        if id:
            transaction = Transaction.query.get_or_404(id)
            transaction_data = {
                'id': transaction.id,
                'user_id': transaction.user_id,
                'amount': str(transaction.amount),
                'transaction_type': transaction.transaction_type,
                'category_id': transaction.category_id,
                'date': transaction.date.strftime('%Y-%m-%d'),
                'description': transaction.description,
                'created_at': transaction.created_at,
                'updated_at': transaction.updated_at
            }
            return jsonify({'transaction': transaction_data})
        else:
            transactions = Transaction.query.all()
            output = []
            for transaction in transactions:
                transaction_data = {
                    'id': transaction.id,
                    'user_id': transaction.user_id,
                    'amount': str(transaction.amount),
                    'transaction_type': transaction.transaction_type,
                    'category_id': transaction.category_id,
                    'date': transaction.date.strftime('%Y-%m-%d'),
                    'description': transaction.description,
                    'created_at': transaction.created_at,
                    'updated_at': transaction.updated_at
                }
                output.append(transaction_data)
            return jsonify({'transactions': output})

    def post(self):
        data = request.get_json()
        new_transaction = Transaction(
            user_id=data.get('user_id'),
            amount=data.get('amount'),
            transaction_type=data.get('transaction_type'),
            category_id=data.get('category_id'),
            date=data.get('date'),
            description=data.get('description')
        )
        db.session.add(new_transaction)
        db.session.commit()
        return {'message': 'Transaction added successfully'}, 201

    def put(self, id):
        data = request.get_json()
        transaction = Transaction.query.get_or_404(id)

        transaction.user_id = data.get('user_id', transaction.user_id)
        transaction.amount = data.get('amount', transaction.amount)
        transaction.transaction_type = data.get('transaction_type', transaction.transaction_type)
        transaction.category_id = data.get('category_id', transaction.category_id)
        transaction.date = data.get('date', transaction.date)
        transaction.description = data.get('description', transaction.description)

        db.session.commit()
        return {'message': 'Transaction updated successfully'}

    def delete(self, id):
        transaction = Transaction.query.get_or_404(id)
        db.session.delete(transaction)
        db.session.commit()
        return {'message': 'Transaction deleted successfully'}

api.add_resource(TransactionResource, '/transactions', '/transactions/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)