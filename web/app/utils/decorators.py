from functools import wraps
from flask import request
from app.utils.helpers import make_json_response, get_id_from_jwt
from app.models import User
from os import environ
from app import revoked_tokens_cache


def creds_required(f):
    '''
    Requires a request to include a user's credentials in the request body
    before carrying out the logic of the route.
    '''
    @wraps(f)
    def decorated_function(*args, **kwargs):
        request_data = request.get_json()

        valid_request = request_data and request_data.get("email")
        valid_request = valid_request and request_data.get("password")

        if valid_request:
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
                user_id = get_id_from_jwt(access_token,
                                          environ.get("ACCESS_TOKEN_SECRET"))

                kwargs["user_id"] = user_id
                return f(*args, **kwargs)

            # enforce access_token was valid, expired or malfourmend tokens
            # will cause exceptions to be trhown from get_id_from_jwt
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

        # enforce refresh_token was sent from client
        if request_data and request_data.get("refresh_token"):
            try:
                refresh_token = request_data.get("refresh_token")
                user_id = get_id_from_jwt(refresh_token,
                                          environ.get("REFRESH_TOKEN_SECRET"))

                if revoked_tokens_cache.get(refresh_token[112:]) == b'revoked':
                    msg = "ERROR 401: Invalid refresh token."
                    return make_json_response(status=401, msg=msg)

                current_user = User.query.filter_by(id=user_id).first()
                if current_user.refresh_token:
                    kwargs["current_user"] = current_user
                    return f(*args, **kwargs)

                raise Exception("No refresh token assoctated with this user")

            # enforce refresh_token was valid, expired or malfourmend tokens
            # will cause exceptions to be trhown from get_id_from_jwt
            except Exception as e:
                print(e)
                msg = "ERROR 401: Invalid refresh token."
                return make_json_response(status=401, msg=msg)

        else:
            msg = ("ERROR 400: Must include 'refresh_token' field in request ",
                   "body.")
            return make_json_response(status=400, msg=msg)

    return decorated_function
