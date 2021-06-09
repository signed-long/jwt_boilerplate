from app import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)
    refresh_token = db.Column(db.String(155))
    otp_secret = db.Column(db.String(16))
