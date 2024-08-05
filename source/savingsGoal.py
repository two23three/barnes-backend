from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from models import db, SavingsGoal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:newpassword@localhost/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
api = Api(app)

class SavingsGoalResource(Resource):
    def get(self, id=None):
        if id:
            savings_goal = SavingsGoal.query.get_or_404(id)
            savings_goal_data = {
                'id': savings_goal.id,
                'user_id': savings_goal.user_id,
                'name': savings_goal.name,
                'target_amount': str(savings_goal.target_amount),
                'current_amount': str(savings_goal.current_amount),
                'start_date': savings_goal.start_date.strftime('%Y-%m-%d'),
                'end_date': savings_goal.end_date.strftime('%Y-%m-%d') if savings_goal.end_date else None,
                'description': savings_goal.description,
                'created_at': savings_goal.created_at,
                'updated_at': savings_goal.updated_at
            }
            return jsonify({'savings_goal': savings_goal_data})
        else:
            savings_goals = SavingsGoal.query.all()
            output = []
            for savings_goal in savings_goals:
                savings_goal_data = {
                    'id': savings_goal.id,
                    'user_id': savings_goal.user_id,
                    'name': savings_goal.name,
                    'target_amount': str(savings_goal.target_amount),
                    'current_amount': str(savings_goal.current_amount),
                    'start_date': savings_goal.start_date.strftime('%Y-%m-%d'),
                    'end_date': savings_goal.end_date.strftime('%Y-%m-%d') if savings_goal.end_date else None,
                    'description': savings_goal.description,
                    'created_at': savings_goal.created_at,
                    'updated_at': savings_goal.updated_at
                }
                output.append(savings_goal_data)
            return jsonify({'savings_goals': output})

    def post(self):
        data = request.get_json()
        new_savings_goal = SavingsGoal(
            user_id=data.get('user_id'),
            name=data.get('name'),
            target_amount=data.get('target_amount'),
            current_amount=data.get('current_amount'),
            start_date=data.get('start_date'),
            end_date=data.get('end_date'),
            description=data.get('description')
        )
        db.session.add(new_savings_goal)
        db.session.commit()
        return {'message': 'Savings goal added successfully'}, 201

    def put(self, id):
        data = request.get_json()
        savings_goal = SavingsGoal.query.get_or_404(id)

        savings_goal.user_id = data.get('user_id', savings_goal.user_id)
        savings_goal.name = data.get('name', savings_goal.name)
        savings_goal.target_amount = data.get('target_amount', savings_goal.target_amount)
        savings_goal.current_amount = data.get('current_amount', savings_goal.current_amount)
        savings_goal.start_date = data.get('start_date', savings_goal.start_date)
        savings_goal.end_date = data.get('end_date', savings_goal.end_date)
        savings_goal.description = data.get('description', savings_goal.description)

        db.session.commit()
        return {'message': 'Savings goal updated successfully'}

    def delete(self, id):
        savings_goal = SavingsGoal.query.get_or_404(id)
        db.session.delete(savings_goal)
        db.session.commit()
        return {'message': 'Savings goal deleted successfully'}



if __name__ == '__main__':
    app.run(debug=True)