from flask import make_response, jsonify


def make_json_response(response_dict):
    '''
    Returns a json response given a response_dict. API style is also enforced.

    Parameter: response_dict (dict) - a dictionary to make a json response from.
    '''
    try:
        status_code = response_dict["http_response"]["status"]
        print(type(make_response(jsonify(response_dict), status_code)))
        return make_response(jsonify(response_dict), status_code)
    except KeyError:
        msg = ("\n\n\nAll responses must include a 'http_response':<dict> "
               "field which has a nested 'status':<int> field.\n\n\n")
        print(msg)
        raise
