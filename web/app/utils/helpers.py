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


def create_jwt_for_user(user, key, sec=None, days=None):
    '''
    Creates a access token.

    Parameter: user (User) - A user to create the token for.
    '''
    if sec:
        payload = {"sub": user.id,
                   "exp": datetime.now(timezone.utc) + timedelta(seconds=sec)}
    elif days:
        payload = {"sub": user.id,
                   "exp": datetime.now(timezone.utc) + timedelta(seconds=sec)}
    else:
        msg = "Expiration time must be passed as 'sec' or 'days' argument"
        raise Exception(msg)

    return jwt.encode(payload, key, algorithm="HS256")


def get_id_from_jwt(token, key):
    '''
    Decodes a JWT token.

    Parameters:
        - token (str) - The JWT token.
        - key (str) - The key used to create the token.
    '''

    payload = jwt.decode(token, key, algorithms="HS256")
    return payload["sub"]
