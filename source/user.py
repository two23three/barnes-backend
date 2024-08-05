from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from models import db, User, Role
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:newpassword@localhost/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
api = Api(app)

class UserResource(Resource):
    def get(self, id=None):
        if id:
            user = User.query.get_or_404(id)
            user_data = {
                'id': user.id,
                'name': user.name,
                'phone_number': user.phone_number,
                'email': user.email,
                'role_id': user.role_id,
                'created_at': user.created_at,
                'updated_at': user.updated_at
            }
            return jsonify({'user': user_data})
        else:
            users = User.query.all()
            output = []
            for user in users:
                user_data = {
                    'id': user.id,
                    'name': user.name,
                    'phone_number': user.phone_number,
                    'email': user.email,
                    'role_id': user.role_id,
                    'created_at': user.created_at,
                    'updated_at': user.updated_at
                }
                output.append(user_data)
            return jsonify({'users': output})

    def post(self):
        data = request.get_json()
        name = data.get('name')
        phone_number = data.get('phone_number')
        email = data.get('email')
        password = data.get('password')
        role_id = data.get('role_id')

        password_hash = generate_password_hash(password)

        new_user = User(name=name, phone_number=phone_number, email=email, password_hash=password_hash, role_id=role_id)
        db.session.add(new_user)
        db.session.commit()

        return {'message': 'User created successfully'}, 201

    def put(self, id):
        data = request.get_json()
        user = User.query.get_or_404(id)

        user.name = data.get('name', user.name)
        user.phone_number = data.get('phone_number', user.phone_number)
        user.email = data.get('email', user.email)
        if data.get('password'):
            user.password_hash = generate_password_hash(data['password'])
        user.role_id = data.get('role_id', user.role_id)

        db.session.commit()

        return {'message': 'User updated successfully'}

    def delete(self, id):
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()

        return {'message': 'User deleted successfully'}


if __name__ == '__main__':
    app.run(debug=True)