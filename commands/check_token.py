import os
from flask import request
from ..errors.errors import TokenNotProvidedError, InvalidTokenError


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
        token = os.getenv('APP_TOKEN') or None
        if not token:
            raise Exception('APP_TOKEN not set in environment variables.')
        return token
