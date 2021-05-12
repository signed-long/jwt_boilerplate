from functools import wraps
from flask import make_response, request, jsonify
from app.utils.helpers import make_json_response


def creds_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        request_data = request.get_json()
        if request_data.get("email") and request_data.get("password"):
            return f(*args, **kwargs)
        else:
            response_dict = {
                "http_response": {
                    "message": "Must include 'email' and 'password' fields.",
                    "status": 400
                }
            }
            return make_json_response(response_dict)
    return decorated_function
