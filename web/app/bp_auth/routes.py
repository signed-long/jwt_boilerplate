from flask import Blueprint, request
from app.utils.decorators import creds_required
from app.utils.helpers import make_json_response
from app import bcrypt
from app.models import User
import jwt
import os


bp_auth = Blueprint("bp_auth", __name__)

# Template response json:
# {
#   "message": "test_set does not exist",
#   "details": {},
#   "description": "The reference set does not exist.",
#   "http_response": {
#      "message": "We could not find the resource you requested.",
#       "status": 404
#    }
# }


@bp_auth.route("/test", methods=["GET"])
def test():
    '''

    '''
    return "You are authorized"


@bp_auth.route("/register", methods=["POST"])
def register():
    '''

    '''
    pass


@bp_auth.route("/login", methods=["POST"])
@creds_required
def login():
    '''

    '''
    # pull user from db
    request_data = request.get_json()
    user = User.query.filter_by(email=request_data["email"]).first()

    # authenticate user and return access token
    if user and bcrypt.check_password_hash(user.password_hash,
                                           request_data["password"]):
        access_token = jwt.encode({"sub": user.id},
                                  os.environ.get("ACCESS_TOKEN_SECRET"),
                                  algorithm="HS256")
        msg = "OK 200: Authentication succesfull."
        return make_json_response(status=200,
                                  msg=msg,
                                  response_dict={"access_token": access_token})

    # user does not exist or entered bad credentials
    msg = "ERROR 401: Authentication failed."
    return make_json_response(status=401, msg=msg)


@bp_auth.route("/logout", methods=["POST"])
def logout():
    '''

    '''
    pass
