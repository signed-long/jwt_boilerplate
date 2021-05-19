from functools import wraps
from flask import request
from app.utils.helpers import make_json_response, decode_jwt_token
from app.models import User
from os import environ


def creds_required(f):
    '''
    Requires a request to include a user's credentials in the request body
    before carrying out the logic of the route.
    '''
    @wraps(f)
    def decorated_function(*args, **kwargs):
        request_data = request.get_json()

        # enforce
        if request_data.get("email") and request_data.get("password"):
            return f(*args, **kwargs)
        else:
            msg = ("ERROR 400: Must include 'email' and 'password' ",
                   "fields in request body.")
            return make_json_response(status=400, msg=msg)

    return decorated_function


def access_token_required(f):
    '''
    Requires a request to include a valid access token in the request body
    before carrying out the logic of the route.
    '''
    @wraps(f)
    def decorated_function(*args, **kwargs):

        # get access_token from request body
        access_token = request.headers.get("Authorization")

        # enforce access_token was sent from client
        if access_token and access_token.startswith("Bearer"):
            access_token = access_token.split(" ")[1]

            try:
                user_id = decode_jwt_token(access_token,
                                           environ.get("ACCESS_TOKEN_SECRET"))
                current_user = User.query.filter_by(id=user_id).first()

                if current_user:
                    kwargs["current_user"] = current_user
                    return f(*args, **kwargs)

                raise Exception

            # enforce access_token was valid, expired or malfourmend tokens
            # will cause exceptions to be trhown from decode_jwt_token
            except Exception:
                msg = ("ERROR 401: Invalid access token. Ensure token is in the"
                       " request's 'Authorization' header in the form:"
                       " 'Bearer token_here'")
                return make_json_response(status=401, msg=msg)

        else:
            msg = ("ERROR 401: Invalid access token. Ensure token is in the"
                   " request's 'Authorization' header in the form:"
                   " 'Bearer token_here'")
            return make_json_response(status=401, msg=msg)

    return decorated_function


def refresh_token_required(f):
    '''
    Requires a request to include a valid refresh token in the request body
    before carrying out the logic of the route.
    '''
    @wraps(f)
    def decorated_function(*args, **kwargs):

        # get refresh_token from request body
        request_data = request.get_json()
        refresh_token = request_data.get("refresh_token")

        # enforce refresh_token was sent from client
        if refresh_token:
            try:
                user_id = decode_jwt_token(refresh_token,
                                           environ.get("REFRESH_TOKEN_SECRET"))
                current_user = User.query.filter_by(id=user_id).first()

                if current_user.refresh_token:
                    kwargs["current_user": current_user]
                    return f(*args, **kwargs)

                raise Exception

            # enforce refresh_token was valid, expired or malfourmend tokens
            # will cause exceptions to be trhown from decode_jwt_token
            except Exception:
                msg = "ERROR 401: Invalid refresh token."
                return make_json_response(status=401, msg=msg)

        else:
            msg = ("ERROR 400: Must include 'refresh_token' field in request ",
                   "body.")
            return make_json_response(status=400, msg=msg)

    return decorated_function
