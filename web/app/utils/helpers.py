from flask import make_response, jsonify


def make_json_response(status, msg, response_dict={}):
    '''
    Returns a json response given a response_dict. API style is also enforced.

    Parameter: response_dict (dict) - a dictionary to make a json response from.
    '''
    response = {
        "http_response": {
            "message": msg,
            "status": status
        },
        "data": {
            **response_dict
        }
    }
    status_code = response["http_response"]["status"]
    return make_response(jsonify(response), status_code)
