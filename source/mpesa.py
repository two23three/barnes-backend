import requests
from requests.auth import HTTPBasicAuth
from flask import Blueprint, jsonify, request
from models import db, User, SavingsGoal 
from decimal import Decimal, InvalidOperation

mpesa_bp = Blueprint('mpesa', __name__)

consumer_key = 'ea0HATa5psrjBgZTqYtFnEkDWV95OJpejEma41qDiSxvwHHD'
consumer_secret = 'GYejBdnK6hDdpgTCjPaG5tAeM9pK2xkn9ghASvO20g3UAs6vQMuupj6HY221j0SP'

def generate_access_token(consumer_key, consumer_secret):
    api_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(api_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    json_response = response.json()
    access_token = json_response['access_token']
    return access_token

def get_user_by_id(user_id):
    """
    Fetches user details from the database by user_id.

    :param user_id: ID of the user.
    :return: A dictionary containing user details or None if the user is not found.
    """
    user = User.query.filter_by(id=user_id).first()
    if user:
        return {
            'id': user.id,
            'phone_number': user.phone_number,
            'email': user.email,
            'name': user.name
        }
    return None

@mpesa_bp.route('/home/', methods=['GET'])
def home():
    return jsonify({'message': 'MPESA API home'})

@mpesa_bp.route('/token', methods=['GET'])
def get_token():
    try:
        token = generate_access_token(consumer_key, consumer_secret)
        return jsonify({'access_token': token})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@mpesa_bp.route('/register_urls', methods=['POST'])
def register_urls():
    try:
        access_token = generate_access_token(consumer_key, consumer_secret)
        api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
        headers = {"Authorization": "Bearer %s" % access_token}
        request_data = {
            "ShortCode": "600987", 
            "ResponseType": "Completed",
            "ConfirmationURL": "https://barnes.onrender.com/m/confirmation",
            "ValidationURL": "https://barnes.onrender.com/m/validation"
        }
        response = requests.post(api_url, json=request_data, headers=headers)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@mpesa_bp.route('/validation', methods=['POST'])
def validation():
    data = request.get_json()
    # Process validation logic here
    return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"})

@mpesa_bp.route('/confirmation', methods=['POST'])
def confirmation():
    data = request.get_json()
    phone_number = data.get('MSISDN')
    amount = data.get('Amount')

    try:
        amount = Decimal(amount)  # Convert the amount to Decimal
    except (ValueError, InvalidOperation) as e:
        return jsonify({"ResultCode": 1, "ResultDesc": "Invalid amount format"}), 400

    # Find the user associated with the phone number
    user = User.query.filter_by(phone_number=phone_number).first()
    if user:
        # Update the user's savings goal
        savings_goal = SavingsGoal.query.filter_by(user_id=user.id).first()
        if savings_goal:
            savings_goal.current_amount += amount
            db.session.commit()
            return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"})
    
    return jsonify({"ResultCode": 1, "ResultDesc": "Failed"}), 400


@mpesa_bp.route('/simulate', methods=['POST'])
def simulate():
    try:
        access_token = generate_access_token(consumer_key, consumer_secret)
        api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate"
        headers = {"Authorization": "Bearer %s" % access_token}
        request_data = {
            "ShortCode": "600987",
            "CommandID": "CustomerPayBillOnline",
            "Amount": "100",
            "Msisdn": "254708374149",
            "BillRefNumber": "TestAPI"
        }
        response = requests.post(api_url, json=request_data, headers=headers)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@mpesa_bp.route('/stk_push', methods=['POST'])
def stk_push():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        amount = data.get('amount')

        # Validate the amount 
        if not amount or not isinstance(amount, (int, float)) or amount <= 0:
            return jsonify({'error': 'Invalid amount'}), 400

        # Fetching the user's details using user_id
        user = get_user_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        phone_number = user.get('phone_number')
        if not phone_number:
            return jsonify({'error': 'Phone number not found for the user'}), 404

        access_token = generate_access_token(consumer_key, consumer_secret)
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {
            "Authorization": "Bearer %s" % access_token,
            "Content-Type": "application/json"
        }
        request_data = {
            "BusinessShortCode": 174379,
            "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjQwODA4MTIxMzI4",
            "Timestamp": "20240808121328",
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone_number,
            "PartyB": 174379,
            "PhoneNumber": phone_number,
            "CallBackURL": "https://mydomain.com/path",
            "AccountReference": "Barnes",
            "TransactionDesc": "Savings"
        }
        response = requests.post(api_url, json=request_data, headers=headers)
        response_data = response.json()

        if response_data.get('ResponseCode') == '0': 
            # Update the user's savings goal
            savings_goals = SavingsGoal.query.filter_by(user_id=user_id).all()
            for goal in savings_goals:
                goal.current_amount += amount
                db.session.add(goal)
            db.session.commit()
            return jsonify({'message': 'STK push successful', 'data': response_data})
        else:
            return jsonify({'error': 'STK push failed', 'data': response_data}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
