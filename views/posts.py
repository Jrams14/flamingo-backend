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

@app.route('/posts', methods=['POST'])
@token_required
def create_post(current_user):
    data = request.get_json()

    print(current_user.username)

    post = Post(user_id = current_user.public_id, spotify_uri = data['spotify_uri'], 
        description = data['description'])
    db.session.add(post)
    db.session.commit()

    post_data = {}
    post_data['id'] = post.id
    post_data['spotify_uri'] = post.spotify_uri
    post_data['description'] = post.description

    response_object = {
            'status': 'success',
            'post': post_data
        }

    return make_response(jsonify(response_object)), 200

@app.route('/posts/<id>', methods=['GET'])
@token_required
def get_post(current_user, id):
    post = Post.query.filter_by(id = id).first()

    if not post:
        response_object = {
            'status': 'fail',
            'message': 'No post found'
        }
        return jsonify(response_object)

    post_data = {}
    post_data['id'] = post.id
    post_data['spotify_uri'] = post.spotify_uri
    post_data['description'] = post.description

    response_object = {
            'status': 'success',
            'post': post_data
        }

    return make_response(jsonify(response_object)), 200

@app.route('/posts', methods=['GET'])
@token_required
def get_dashboard_posts(current_user):
    posts = Post.query.order_by(Post.created_date.desc()).all()

    if not posts:
        response_object = {
            'status': 'fail',
            'message': 'No posts found'
        }
        return jsonify(response_object)

    output = []

    for post in posts:
        post_data = {}
        post_data['id'] = post.id
        post_data['user_id'] = post.user_id
        post_data['spotify_uri'] = post.spotify_uri
        post_data['description'] = post.description
        output.append(post_data)

    response_object = {
            'status': 'success',
            'posts': output
        }

    return make_response(jsonify(response_object)), 200

@app.route('/profile/<id>', methods=['GET'])
@token_required
def get_profile_posts(current_user, id):
    posts = Post.query.filter_by(user_id = id).order_by(Post.created_date.desc())

    if not posts:
        response_object = {
            'status': 'fail',
            'message': 'No posts were found'
        }
        return jsonify(response_object)
    output = []

    for post in posts:
        post_data = {}
        post_data['id'] = post.id
        post_data['user_id'] = post.user_id
        post_data['spotify_uri'] = post.spotify_uri
        post_data['description'] = post.description
        output.append(post_data)

    response_object = {
            'status': 'success',
            'posts': output
        }

    return make_response(jsonify(response_object)), 200