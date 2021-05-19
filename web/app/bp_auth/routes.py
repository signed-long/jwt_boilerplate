from flask import Blueprint, request
from app import bcrypt, db
from app.models import User
from app.utils.helpers import (
    make_json_response,
    create_access_token,
    create_refresh_token
)
from app.utils.decorators import (
    creds_required,
    access_token_required,
    refresh_token_required
)


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
def test():
    '''

    '''
    return kwargs["current_user"].email


@bp_auth.route("/register", methods=["POST"])
@creds_required
def register():
    '''

    '''
    request_data = request.get_json()
    email = request_data["email"]
    pw_hash = bcrypt.generate_password_hash(request_data["password"])

    new_user = User(email=email, password_hash=pw_hash.decode("utf-8"))
    db.session.add(new_user)
    db.session.commit()

    msg = "OK 200: Registration successful"
    return make_json_response(status=200, msg=msg)


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

        access_token = create_access_token(user)
        refresh_token = create_refresh_token(user)
        tokens = {"access_token": access_token, "refresh_token": refresh_token}
        msg = "OK 200: Authentication successful"
        return make_json_response(status=200, msg=msg, response_dict=tokens)

    # user does not exist or entered bad credentials
    msg = "ERROR 401: Authentication failed."
    return make_json_response(status=401, msg=msg)


@bp_auth.route("/logout", methods=["POST"])
def logout():
    '''

    '''
    pass


@bp_auth.route("/refresh", methods=["POST"])
@refresh_token_required
def refresh():
    '''

    '''
    pass
