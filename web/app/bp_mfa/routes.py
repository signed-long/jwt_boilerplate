from flask import Blueprint, request
import pyopt

bp_mfa = Blueprint("bp_mfa", __name__)


@bp_mfa.route("/setup_mfa", methods=["POST"])
def setup_otp():
    '''

    '''

    pass
