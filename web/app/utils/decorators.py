from functools import wraps
from flask import request
from app.utils.helpers import make_json_response, decode_jwt_token
from app.models import User


def creds_required(f):
    '''

    '''
    @wraps(f)
    def decorated_function(*args, **kwargs):
        request_data = request.get_json()
        if request_data.get("email") and request_data.get("password"):
            return f(*args, **kwargs)
        else:
            msg = "ERROR 400: Must include 'email' and 'password' fields."
            return make_json_response(status=400, msg=msg)
    return decorated_function


def access_token_required(f):
    '''

    '''
    @wraps(f)
    def decorated_function(*args, **kwargs):
        request_data = request.get_json()
        access_token = request_data.get("access_token")

        if access_token:
            try:
                user_id = decode_jwt_token(access_token)
                current_user = User.query.filter_by(id=user_id).first()

                if current_user:
                    return f(current_user, *args, **kwargs)

                raise Exception

            except Exception:
                msg = "ERROR 401: Invalid access token."
                return make_json_response(status=401, msg=msg)

        else:
            msg = "ERROR 400: Must include 'access_token' field."
            return make_json_response(status=400, msg=msg)

    return decorated_function


def refresh_token_required(f):
    '''

    '''
    @wraps(f)
    def decorated_function(*args, **kwargs):
        request_data = request.get_json()
        refresh_token = request_data.get("refresh_token")

        if refresh_token:
            try:
                user_id = decode_jwt_token(refresh_token, type="refresh")
                current_user = User.query.filter_by(id=user_id).first()

                if current_user.refresh_token:
                    return f(current_user, *args, **kwargs)

                raise Exception

            except Exception:
                msg = "ERROR 401: Invalid refresh token."
                return make_json_response(status=401, msg=msg)

        else:
            msg = "ERROR 400: Must include 'refresh_token' field."
            return make_json_response(status=400, msg=msg)

    return decorated_function
