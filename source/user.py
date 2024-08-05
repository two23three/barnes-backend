from flask import request, jsonify
from flask_restful import Resource
from models import db, User
from werkzeug.security import generate_password_hash
import uuid


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
                'updated_at': user.updated_at,
                'referral_code': user.referral_code,
                'referred_by': user.referred_by
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
                    'updated_at': user.updated_at,
                    'referral_code': user.referral_code,
                    'referred_by': user.referred_by
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
        referral_code = data.get('referral_code')

        password_hash = generate_password_hash(password)

        # Check if referral code exists and is valid
        referred_by_user = None
        if referral_code:
            referred_by_user = User.query.filter_by(referral_code=referral_code).first()
            if not referred_by_user:
                return {'message': 'Invalid referral code'}, 400

        # Generate a unique referral code for the new user
        new_user_referral_code = str(uuid.uuid4())

        new_user = User(
            name=name,
            phone_number=phone_number,
            email=email,
            password_hash=password_hash,
            role_id=role_id,
            referral_code=new_user_referral_code,
            referred_by=referred_by_user.referral_code if referred_by_user else None
        )
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
    