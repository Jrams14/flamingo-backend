from flask import Flask, request, redirect, jsonify, make_response
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

from views.auth_views import *

if __name__ == '__main__':
    app.run(debug = True)

