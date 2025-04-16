import pytest
from model.blacklist import NewBlacklistJsonSchema, ValidateEmailJsonSchema
from errors.errors import ParamError


class TestNewBlacklistJsonSchema:
    def test_valid_data(self):
        valid_data = {
            "email": "test@example.com",
            "app_uuid": "123e4567-e89b-12d3-a456-426614174000",
            "blocked_reason": "Spamming",
        }
        try:
            NewBlacklistJsonSchema.check(valid_data)
        except Exception as e:
            pytest.fail(f"Unexpected exception raised: {e}")

    def test_missing_required_field(self):
        invalid_data = {
            "app_uuid": "123e4567-e89b-12d3-a456-426614174000",
            "blocked_reason": "Spamming",
        }
        with pytest.raises(ParamError):
            NewBlacklistJsonSchema.check(invalid_data)

    def test_invalid_email(self):
        invalid_data = {
            "email": "invalid-email",
            "app_uuid": "123e4567-e89b-12d3-a456-426614174000",
            "blocked_reason": "Spamming",
        }
        with pytest.raises(ParamError):
            NewBlacklistJsonSchema.check(invalid_data)


class TestValidateEmailJsonSchema:
    def test_valid_data(self):
        valid_data = { "email": "test@example.com" }
        try:
            ValidateEmailJsonSchema.check(valid_data)
        except Exception as e:
            pytest.fail(f"Unexpected exception raised: {e}")

    def test_missing_email(self):
        invalid_data = {}
        with pytest.raises(ParamError):
            ValidateEmailJsonSchema.check(invalid_data)

    def test_invalid_email(self):
        invalid_data = { "email": "invalid-email" }
        with pytest.raises(ParamError):
            ValidateEmailJsonSchema.check(invalid_data)
