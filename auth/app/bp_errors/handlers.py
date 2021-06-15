from flask import Blueprint
from app.utils.helpers import make_json_response

bp_errors = Blueprint('bp_errors', __name__)


@bp_errors.app_errorhandler(404)
def error_404(error):
    '''
    Handels 404 error Page Not Found.
    '''
    msg = ("ERROR 404: Page not found.")
    return make_json_response(status=404, msg=msg)


@bp_errors.app_errorhandler(405)
def error_405(error):
    '''
    Handels 405 error Method not allowed.
    '''
    msg = ("ERROR 405: Method not allowed.")
    return make_json_response(status=405, msg=msg)


@bp_errors.app_errorhandler(500)
def error_500(error):
    '''
    Handels 500 error Internal Error.
    '''
    msg = ("ERROR 500: An error occured on the server.")
    return make_json_response(status=500, msg=msg)
