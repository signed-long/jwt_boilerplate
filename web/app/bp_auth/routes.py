from flask import Blueprint

bp_auth = Blueprint("bp_auth", __name__)


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
def login():
    '''

    '''
    pass


@bp_auth.route("/logout", methods=["POST"])
def logout():
    '''

    '''
    pass
