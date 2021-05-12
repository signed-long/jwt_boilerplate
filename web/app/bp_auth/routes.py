from flask import Blueprint, request, make_response
from app.utils.decorators import creds_required
from app.utils.helpers import make_json_response


bp_auth = Blueprint("bp_auth", __name__)

# Template response json:
# {
#   "message": "test_set does not exist",
#   "details": {},
#   "description": "The reference set does not exist.",
#   "http_response": {
#      "message": "We could not find the resource you requested.",
#       "code": 404
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
    return "login"


@bp_auth.route("/logout", methods=["POST"])
def logout():
    '''

    '''
    pass
