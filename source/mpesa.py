
import requests
from requests.auth import HTTPBasicAuth
from flask import Blueprint, jsonify, request

mpesa_bp = Blueprint('mpesa', __name__)

consumer_key = 'ea0HATa5psrjBgZTqYtFnEkDWV95OJpejEma41qDiSxvwHHD'
consumer_secret = 'GYejBdnK6hDdpgTCjPaG5tAeM9pK2xkn9ghASvO20g3UAs6vQMuupj6HY221j0SP'

def generate_access_token(consumer_key, consumer_secret):
    api_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(api_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    json_response = response.json()
    access_token = json_response['access_token']
    return access_token

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
    # Process confirmation logic here
    return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"})

@mpesa_bp.route('/simulate', methods=['POST'])
def simulate():
    try:
        access_token = generate_access_token(consumer_key, consumer_secret)
        api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate"
        headers = {"Authorization": "Bearer %s" % access_token}
        request_data = {
            "ShortCode": "YOUR_SHORT_CODE",
            "CommandID": "CustomerPayBillOnline",
            "Amount": "100",
            "Msisdn": "254708374149",
            "BillRefNumber": "TestAPI"
        }
        response = requests.post(api_url, json=request_data, headers=headers)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500
