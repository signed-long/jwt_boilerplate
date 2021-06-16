from flask import Blueprint
from app import db
from app.models import User
from app.utils.helpers import (
    make_json_response
)
from app.utils.decorators import (
    access_token_required
)

bp_mfa = Blueprint("bp_mfa", __name__)

@bp_mfa.route("/setup_mfa", methods=["GET"])
@access_token_required
def setup_otp(user_id):
    '''
    Responds with the user's otp_secret in a otp uri.
    '''
    user = User.query.filter_by(id=user_id).first()
    user.set_otp_secret()
    db.session.commit()

    response = {"otp_uri": user.get_totp_uri()}
    msg = "OK 200: OTP URI Provided."
    return make_json_response(status=200, msg=msg, response_dict=response)
