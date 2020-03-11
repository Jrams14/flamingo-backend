from app import app, db
from flask import Flask, request, redirect, jsonify, make_response
import requests
from urllib.parse import urlencode, quote_plus
import uuid
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import datetime
from models import *

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id = data['public_id']).first()
        except:
            return jsonify({'message': 'Token is invalid'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/user', methods=['GET'])
def get_all_users():
    users = User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        output.append(user_data)
    return jsonify({'users': output})

@app.route('/register', methods=['POST'])
def create_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method = 'sha256')

    user = User(public_id = str(uuid.uuid4()), password = hashed_password, first_name = data['first'], last_name = data['last'], username = data['username'])
    db.session.add(user)
    db.session.commit()

    token = jwt.encode({'public_id': user.public_id,'first' : user.first_name, 'last': user.last_name, 'username': user.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes = 30)}, app.config['SECRET_KEY'])

    response_object = {
                    'status': 'success',
                    'message': 'User created',
                    'auth_token': token.decode('UTF-8')
                }
    return make_response(jsonify(response_object)), 200

@app.route('/login', methods = ['POST'])
def login():
    data = request.get_json()

    try:
        user = User.query.filter_by(username = data['username']).first()
        print(user.username)

        if user and check_password_hash(user.password, data['password']):
            token = jwt.encode({'public_id': user.public_id,'first' : user.first_name, 'last': user.last_name, 'username': user.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes = 30)}, app.config['SECRET_KEY'])

            response_object = {
                            'status': 'success',
                            'message': 'Successfully logged in',
                            'auth_token': token.decode('UTF-8')
                        }
            return make_response(jsonify(response_object)), 200

        else:
            response_object = {
                            'status': 'fail',
                            'message': 'User not found',
                        }
            return make_response(jsonify(response_object)), 401

    except Exception as e:
        print(e)
        response_object = {
            'status': 'fail',
            'message': 'Try again'
        }
        return make_response(jsonify(response_object)), 500

@app.route('/user/<public_id>', methods=['GET'])
@token_required
def get_user(current_user, public_id):
    user = User.query.filter_by(public_id = public_id).first()

    if not user:
        return jsonify({'message': 'No user found'})

    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['name'] = user.name
    user_data['password'] = user.password

    return jsonify({'user': user_data})


# @app.route('/auth')
# def authorize():
#     payload = {'client_id': app.config['CLIENT_ID'], 'redirect_uri': app.config['REDIRECT_URL'], 'response_type': 'code'}
#     params = urlencode(payload, quote_via=quote_plus)
#     return redirect(app.config['AUTH_URL'] + params)