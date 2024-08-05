from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from datetime import datetime
from models import db, DebtPayment

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)
api = Api(app)

class DebtPaymentResource(Resource):
    def get(self, id=None):
        if id:
            debt_payment = DebtPayment.query.get_or_404(id)
            debt_payment_data = {
                'id': debt_payment.id,
                'debt_id': debt_payment.debt_id,
                'amount': str(debt_payment.amount),
                'payment_date': debt_payment.payment_date.strftime('%Y-%m-%d'),
                'created_at': debt_payment.created_at.isoformat(),
                'updated_at': debt_payment.updated_at.isoformat()
            }
            return jsonify({'debt_payment': debt_payment_data})
        else:
            debt_payments = DebtPayment.query.all()
            output = []
            for debt_payment in debt_payments:
                debt_payment_data = {
                    'id': debt_payment.id,
                    'debt_id': debt_payment.debt_id,
                    'amount': str(debt_payment.amount),
                    'payment_date': debt_payment.payment_date.strftime('%Y-%m-%d'),
                    'created_at': debt_payment.created_at.isoformat(),
                    'updated_at': debt_payment.updated_at.isoformat()
                }
                output.append(debt_payment_data)
            return jsonify({'debt_payments': output})

    def post(self):
        data = request.get_json()
        debt_id = data.get('debt_id')
        amount = data.get('amount')
        payment_date = datetime.strptime(data.get('payment_date'), '%Y-%m-%d').date()

        new_debt_payment = DebtPayment(debt_id=debt_id, amount=amount, payment_date=payment_date)
        db.session.add(new_debt_payment)
        db.session.commit()

        return {'message': 'Debt payment created successfully'}, 201

    def put(self, id):
        data = request.get_json()
        debt_payment = DebtPayment.query.get_or_404(id)

        debt_payment.debt_id = data.get('debt_id', debt_payment.debt_id)
        debt_payment.amount = data.get('amount', debt_payment.amount)
        debt_payment.payment_date = datetime.strptime(data.get('payment_date', debt_payment.payment_date.strftime('%Y-%m-%d')), '%Y-%m-%d').date()

        db.session.commit()

        return {'message': 'Debt payment updated successfully'}

    def delete(self, id):
        debt_payment = DebtPayment.query.get_or_404(id)
        db.session.delete(debt_payment)
        db.session.commit()

        return {'message': 'Debt payment deleted successfully'}

api.add_resource(DebtPaymentResource, '/debt_payments', '/debt_payments/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)