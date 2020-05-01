from app import db
import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    public_id = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(80))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    username = db.Column(db.String(50), unique = True)
    post = db.relationship("Post")

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.public_id'))
    spotify_uri = db.Column(db.String(50))
    description = db.Column(db.String(120))
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)


