from app import app, db
from flask import Flask, request, redirect, jsonify, make_response
import jwt
import requests
from functools import wraps
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

@app.route('/user/<id>', methods = ["GET"])
@token_required
def get_user_info(current_user, id):
    user = User.query.filter_by(public_id = id).first()

    if not user:
        response_object = {
            'status': 'fail',
            'message': 'No user found'
        }
        return jsonify(response_object)

    user_data = {}
    user_data['id'] = user.public_id
    user_data['first_name'] = user.first_name
    user_data['last_name'] = user.last_name
    user_data['username'] = user.username

    response_object = {
            'status': 'success',
            'user': user_data
        }

    return make_response(jsonify(response_object)), 200

@app.route('/search/<username>', methods=['GET'])
@token_required
def get_all_users(current_user, username):
    search = "%{}%".format(username)
    users = User.query.filter(User.username.like(search)).all()

    output = []

    for user in users:
        user_data = {}
        user_data['id'] = user.public_id
        user_data['first'] = user.first_name
        user_data['last'] = user.last_name
        user_data['username'] = user.username
        output.append(user_data)

    return jsonify({'users': output})




