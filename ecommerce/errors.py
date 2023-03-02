from flask import jsonify


def page_not_found(error):
    response = {
        'status': 'error',
        'message': 'Page not found'
    }
    return jsonify(response), 404
