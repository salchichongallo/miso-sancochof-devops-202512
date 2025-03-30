import os
from flask import request
from errors.errors import ApiError, TokenNotProvidedError, InvalidTokenError


class CheckTokenCommand:
    @staticmethod
    def execute():
        auth_header = request.headers.get('Authorization') or None

        if not auth_header:
            raise TokenNotProvidedError()

        app_token = CheckTokenCommand.get_app_token()
        token = 'Bearer ' + app_token
        if auth_header != token:
            raise InvalidTokenError()


    @staticmethod
    def get_app_token():
        token = os.getenv('SECRET_TOKEN') or None
        if not token:
            error = ApiError()
            error.code = 500
            error.description = 'SECRET_TOKEN not set in environment variables.'
            raise error
        return token
