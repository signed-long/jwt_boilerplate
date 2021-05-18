from functools import wraps
from flask import request
from app.utils.helpers import make_json_response


def creds_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        request_data = request.get_json()
        if request_data.get("email") and request_data.get("password"):
            return f(*args, **kwargs)
        else:
            msg = "ERROR 400: Must include 'email' and 'password' fields."
            return make_json_response(status=400, msg=msg)
    return decorated_function
