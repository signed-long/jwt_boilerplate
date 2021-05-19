from flask import make_response, jsonify
import jwt
from os import environ
from datetime import datetime, timedelta, timezone


def make_json_response(status, msg, response_dict={}):
    '''
    Returns a JSON response given a response_dict. Required fields are passed as
    arguments, any other data is passed in as 'response_dict'.

    Parameters:
        - status (int) - Status code of the response.
        - msg (str) - Additional information for client.
        - response_dict (dict) - A dictionary that will be returned in the
          'data' field of the response.
    '''
    response = {
        "http_response": {
            "message": msg,
            "status": status
        },
        "data": {
            **response_dict
        }
    }
    status_code = response["http_response"]["status"]
    return make_response(jsonify(response), status_code)


def create_access_token(user):
    '''
    Creates a access token.

    Parameter: user (User) - A user to create the token for.
    '''
    token_life = int(environ.get("ACCESS_TOKEN_EXP_MINS"))
    payload = {"sub": user.id,
               "exp": datetime.now(timezone.utc) + timedelta(minutes=token_life)}

    return jwt.encode(payload, environ.get("ACCESS_TOKEN_SECRET"),
                      algorithm="HS256")


def create_refresh_token(user):
    '''
    Creates a refresh token.

    Parameter: user (User) - A user to create the token for.
    '''
    token_life = int(environ.get("REFRESH_TOKEN_EXP_DAYS"))
    payload = {"sub": user.id,
               "exp": datetime.now(timezone.utc) + timedelta(minutes=token_life)}

    return jwt.encode(payload, environ.get("REFRESH_TOKEN_SECRET"),
                      algorithm="HS256")


def decode_jwt_token(token, key):
    '''
    Decodes a JWT token.

    Parameters:
        - token (str) - The JWT token.
        - key (str) - The key used to create the token.
    '''

    payload = jwt.decode(token, key, algorithms="HS256")
    return payload["sub"]
