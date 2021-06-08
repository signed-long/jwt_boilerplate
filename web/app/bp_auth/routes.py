from flask import Blueprint, request
from os import environ
from app import bcrypt, db, revoked_tokens_cache
from app.models import User
import jwt
from app.utils.helpers import (
    make_json_response,
    create_jwt_for_user,
    revoke_token
)
from app.utils.decorators import (
    creds_required,
    access_token_required,
    refresh_token_required
)
import time
from datetime import datetime, timezone


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
@access_token_required
def test(user_id):
    '''
    Test route to test and authorization required endpoint.
    '''
    return str(user_id)


@bp_auth.route("/register", methods=["POST"])
@creds_required
def register():
    '''
    Creates a new user in the db.
    '''
    request_data = request.get_json()
    email = request_data["email"]
    pw_hash = bcrypt.generate_password_hash(request_data["password"])

    new_user = User(email=email, password_hash=pw_hash.decode("utf-8"))
    db.session.add(new_user)
    db.session.commit()

    msg = "OK 201: Registration successful"
    return make_json_response(status=201, msg=msg)


@bp_auth.route("/login", methods=["POST"])
@creds_required
def login():
    '''
    Authenticates a client and responds with access and refresh tokens.
    '''
    # pull user from db
    request_data = request.get_json()
    user = User.query.filter_by(email=request_data["email"]).first()

    # authenticate user and return access token
    if user and bcrypt.check_password_hash(user.password_hash,
                                           request_data["password"]):

        exp = int(environ.get("ACCESS_TOKEN_EXP_SEC"))
        access_token = create_jwt_for_user(user.id,
                                           environ.get("ACCESS_TOKEN_SECRET"),
                                           sec=exp)
        exp = int(environ.get("REFRESH_TOKEN_EXP_DAYS"))
        refresh_token = create_jwt_for_user(user.id,
                                            environ.get("REFRESH_TOKEN_SECRET"),
                                            days=exp)

        # save user's refresh token
        user.refresh_token = refresh_token
        db.session.commit()

        tokens = {"access_token": access_token, "refresh_token": refresh_token}
        msg = "OK 200: Authentication successful"
        return make_json_response(status=200, msg=msg, response_dict=tokens)

    # user does not exist or entered bad credentials
    msg = "ERROR 401: Authentication failed."
    return make_json_response(status=401, msg=msg)


@bp_auth.route("/logout", methods=["POST"])
@refresh_token_required
def logout(current_user):
    '''
    Deletes a user's refresh token from the db and adds it to the revoked cache.
    '''
    # revoke_token(access_token, environ.get("ACCESS_TOKEN_SECRET"))
    revoke_token(current_user.refresh_token, environ.get("REFRESH_TOKEN_SECRET"))
    current_user.refresh_token = None
    db.session.commit()

    msg = "OK 200: Refresh token revoked."
    return make_json_response(status=200, msg=msg)


@bp_auth.route("/refresh", methods=["GET"])
@refresh_token_required
def refresh(current_user):
    '''
    Returns a fresh access token given a valid refresh token.
    '''
    exp = int(environ.get("ACCESS_TOKEN_EXP_SEC"))
    access_token = create_jwt_for_user(current_user.id,
                                       environ.get("ACCESS_TOKEN_SECRET"),
                                       sec=exp)

    tokens = {"access_token": access_token}
    msg = "OK 200: Access token refreshed succesfully."
    return make_json_response(status=200, msg=msg, response_dict=tokens)


@bp_auth.route("/redis_test", methods=["GET"])
def redis():
    '''
    Returns a fresh access token given a valid refresh token.
    '''
    revoked_tokens_cache.set("refresh_token_hash", "revoked", ex=10)
    print(revoked_tokens_cache.get("refresh_token_hash"))
    time.sleep(20)
    print(revoked_tokens_cache.get("refresh_token_hash"))

    return "name"
