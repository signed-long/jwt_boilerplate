from app import db
import pyotp
from app import bcrypt


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)
    refresh_token = db.Column(db.String(155))
    otp_secret = db.Column(db.String(32))

    def check_pw_hash(self, pt_password):
        '''
        Checks a given password against the user's password hash.
        '''
        return bcrypt.check_password_hash(self.password_hash, pt_password)

    def set_pw_hash(self, pt_password):
        '''
        Sets a user's password hash given a password.
        '''
        pw_hash = bcrypt.generate_password_hash(pt_password)
        self.password_hash = pw_hash.decode("utf-8")

    def get_totp_uri(self):
        '''
        Returns a otpauth uri that can be shown as a QR code on the client.
        '''
        return 'otpauth://totp/JWT-Service:{0}?secret={1}&issuer=JWT-Service' \
            .format(self.id, self.otp_secret)

    def verify_totp(self, token):
        '''
        Verify's a given TOTP with the user's otp_secret.
        '''
        totp = pyotp.TOTP(self.otp_secret)
        return totp.verify(token)

    def set_otp_secret(self):
        '''
        Sets the user's otp_secret with a random value.
        '''
        self.otp_secret = pyotp.random_base32()
