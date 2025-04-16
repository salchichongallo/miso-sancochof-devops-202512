from errors.errors import ApiError, ParamError, DuplicatedEmailError, TokenNotProvidedError, InvalidTokenError


def test_api_error_default_values():
    error = ApiError()
    assert error.code == 422
    assert error.description == "Default message"


def test_param_error_custom_description():
    error = ParamError("Custom description")
    assert error.code == 400
    assert error.description == "Custom description"


def test_param_error_first_from():
    messages = {"field1": ["Validation error 1", "Validation error 2"]}
    error = ParamError.first_from(messages)
    assert isinstance(error, ParamError)
    assert error.code == 400
    assert error.description == "field1: Validation error 1"


def test_duplicated_email_error():
    error = DuplicatedEmailError()
    assert error.code == 409
    assert error.description == "No se pudo crear la cuenta. Está duplicado el email."


def test_token_not_provided_error():
    error = TokenNotProvidedError()
    assert error.code == 403
    assert error.description == "Token not provided."


def test_invalid_token_error():
    error = InvalidTokenError()
    assert error.code == 401
    assert error.description == "Invalid token."
