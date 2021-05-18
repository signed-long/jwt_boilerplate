from flask import make_response, jsonify
import jwt
import os
from datetime import datetime, timedelta, timezone


def make_json_response(status, msg, response_dict={}):
    '''
    Returns a json response given a response_dict. API style is also enforced.

    Parameter: response_dict (dict) - a dictionary to make a json response from.
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

    '''
    token_life = int(os.environ.get("TOKEN_EXPIRATION_TIME"))
    payload = {"sub": user.id,
               "exp": datetime.now(timezone.utc) + timedelta(seconds=token_life)}

    return jwt.encode(payload, os.environ.get("ACCESS_TOKEN_SECRET"),
                      algorithm="HS256")


def create_refresh_token(user):
    '''

    '''
    payload = {"sub": user.id}

    return jwt.encode(payload, os.environ.get("REFRESH_TOKEN_SECRET"),
                      algorithm="HS256")


def decode_jwt_token(token, type="access"):
    '''

    '''
    if type == "access":
        payload = jwt.decode(token, os.environ.get("ACCESS_TOKEN_SECRET"))
    elif type == "refresh":
        payload = jwt.decode(token, os.environ.get("REFRESH_TOKEN_SECRET"))

    return payload["sub"]
