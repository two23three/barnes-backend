from flask import request, jsonify
from flask_restful import Resource
from models import db, User, FinancialReport
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
                'referred_by': user.referred_by,
                'referred_by_name': user.referring_user.name if user.referring_user else None
            }
            return jsonify({'user': user_data})
        else:
            users = User.query.all()
            output = [
                {
                    'id': user.id,
                    'name': user.name,
                    'phone_number': user.phone_number,
                    'email': user.email,
                    'role_id': user.role_id,
                    'created_at': user.created_at,
                    'updated_at': user.updated_at,
                    'referral_code': user.referral_code,
                    'referred_by': user.referred_by,
                    'referred_by_name': user.referring_user.name if user.referring_user else None
                }
                for user in users
            ]
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

        # Generate a unique referral code for the new user using their username
        new_user_referral_code = f"{name[:3]}-{str(uuid.uuid4())[:4]}"

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

class UsersFinancialReport(Resource):
    def get(self, user_id, report_id=None):
        if report_id:
            report = FinancialReport.query.filter_by(user_id=user_id, id=report_id).first_or_404()
            report_data = {
                'id': report.id,
                'user_id': report.user_id,
                'report_type': report.report_type,
                'report_data': report.report_data,
                'created_at': report.created_at,
                'updated_at': report.updated_at
            }
            return jsonify({'financial_report': report_data})
        else:
            reports = FinancialReport.query.filter_by(user_id=user_id).all()
            output = []
            for report in reports:
                report_data = {
                    'id': report.id,
                    'user_id': report.user_id,
                    'report_type': report.report_type,
                    'report_data': report.report_data,
                    'created_at': report.created_at,
                    'updated_at': report.updated_at
                }
                output.append(report_data)
            return jsonify({'financial_reports': output})

    def post(self, user_id):
        data = request.get_json()
        report_type = data.get('report_type')
        report_data = data.get('report_data')

        user = User.query.get_or_404(user_id)

        new_report = FinancialReport(
            user_id=user_id,
            report_type=report_type,
            report_data=report_data
        )
        db.session.add(new_report)
        db.session.commit()

        return {'message': 'Financial report created successfully'}, 201

    def put(self, user_id, report_id):
        data = request.get_json()
        report = FinancialReport.query.filter_by(user_id=user_id, id=report_id).first_or_404()

        report.report_type = data.get('report_type', report.report_type)
        report.report_data = data.get('report_data', report.report_data)

        db.session.commit()

        return {'message': 'Financial report updated successfully'}

    def delete(self, user_id, report_id):
        report = FinancialReport.query.filter_by(user_id=user_id, id=report_id).first_or_404()
        db.session.delete(report)
        db.session.commit()

        return {'message': 'Financial report deleted successfully'}
