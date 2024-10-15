from flask import json, request, jsonify, session, current_app
from flask_login import login_user, logout_user, current_user
from webapp.models import User
from webapp.account import bp  

import time #for slowing down responses in testing
import stripe

@bp.route('/me')
def me():
    if current_user.is_authenticated:
        return jsonify({'authenticated': True, 
                        'userId': current_user.id, 
                        'searches': current_app.config['FREE_SEARCH_LIMIT'] - current_user.get_current_month_search_count(), 
                        'userName': current_user.first_name,
                        'subscriptionType': current_user.subscription_type
                        })
    else:
        return jsonify({'authenticated': False}), 200  

@bp.route('/signup', methods=['POST']) 
def signup():
    data = request.get_json()
    time.sleep(5)

    if not data:
        return jsonify({'error': 'Invalid request data'}), 400  # Bad Request

    first_name = data.get('firstName')
    last_name = data.get('lastName')
    email = data.get('email')
    password = data.get('password')
    subscription_type = 'free'

    if not email or not password or not first_name or not last_name:
        return jsonify({'error': 'Email and password are required'}),


    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'error': 'User already exists'}), 409

    user = User.create_user(first_name, last_name, email, password, subscription_type)
    
    login_user(user)  # Log in the user
    return jsonify({'message': 'Sign up successful!', 'user_id': user.id}), 201
    
@bp.route('/login', methods=['POST'])
def login():
    time.sleep(5)
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Invalid request data'}), 400

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'Invalid email or password'}), 401  

    if not user.check_password(user, password):  
        return jsonify({'error': 'Invalid email or password'}), 401  

    login_user(user)
    return jsonify({'message': 'Login successful!', 'user_id': user.id}), 200

@bp.route('/logout', methods=['POST'])
def logout():
     logout_user()
     session.clear()
     response = jsonify({'message': 'Logged out successfully!'})
     response.delete_cookie('session', samesite='None', secure=True, httponly=True)
     return response, 200

@bp.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    data = request.get_json()
    user_id = data['userId']

    # Create a Stripe Checkout session
    stripe.api_key = current_app.config['STRIPE_KEY']
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': current_app.config['STRIPE_PRICE_ID'], 
            'quantity': 1,
        }],
        mode='subscription', 
        success_url=current_app.config['STRIPE_SUCCESS_URL'],
        cancel_url=current_app.config['STRIPE_CANCEL_URL'],
        metadata={'user_id': user_id}  
    )

    return jsonify({'id': session.id}), 200

@bp.route('/stripe-webhook', methods=['POST'])
def stripe_webhook():
    payload = request.data.decode("utf-8")  
    sig_header = request.headers.get('Stripe-Signature') 
    endpoint_secret = current_app.config['STRIPE_WEBHOOK_SECRET']  

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )

        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            user_id = session['metadata']['user_id'] 

            user = User.query.get(user_id)

            user.subscription_type = 'premium'
            db.session.commit()
    except ValueError as e:
        # Invalid payload
        return jsonify({'error': 'Invalid payload'}), 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return jsonify({'error': 'Invalid signature'}), 400

    return jsonify({'status': 'success'}), 200  # Return a 200 OK response to Stripe