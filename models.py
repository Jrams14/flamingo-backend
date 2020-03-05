from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    public_id = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(80))
    name = db.Column(db.String(50))