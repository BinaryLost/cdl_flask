from flask import jsonify
from http import HTTPStatus


def convert_form_errors_to_string(errors):
    """
    Convertit un dictionnaire d'erreurs de formulaire en une chaîne de caractères.
    """
    error_messages = []
    for field, messages in errors.items():
        for message in messages:
            error_messages.append(f"{field}: {message}")
    return "\n".join(error_messages)


def bad_request(error):
    response = {
        'status': 'error',
        'errors': str(error)
    }
    return jsonify(response), HTTPStatus.BAD_REQUEST


def not_found(error):
    response = {
        'status': 'error',
        'errors': 'Not Found'
    }
    return jsonify(response), HTTPStatus.NOT_FOUND


def internal_server_error(error):
    response = {
        'status': 'error',
        'errors': 'Internal Server Error'
    }
    return jsonify(response), HTTPStatus.INTERNAL_SERVER_ERROR


def limit_error(e):
    response = {
        'status': 'error',
        'errors': 'File too large'
    }
    return jsonify(response), HTTPStatus.REQUEST_ENTITY_TOO_LARGE
