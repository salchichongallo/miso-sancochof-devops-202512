class ApiError(Exception):
    code = 422
    description = "Default message"


class ParamError(ApiError):
    code = 400

    def __init__(self, description):
        self.description = description

    @staticmethod
    def first_from(messages):
        (field, validations) = list(messages.items())[0]
        return ParamError(f"{field}: {validations[0]}")


class DuplicatedEmailError(ApiError):
    code = 409
    description = "No se pudo crear la cuenta. Está duplicado el email."


class TokenNotProvidedError(ApiError):
    code = 403
    description = 'Token not provided.'


class InvalidTokenError(ApiError):
    code = 401
    description = 'Invalid token.'
