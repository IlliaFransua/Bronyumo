import re

from rest_framework import serializers

from Bronyumo.settings import db_dsn
from .BaseValidator import BaseValidator
from ..managers import CompanyManager


class EmailValidator(BaseValidator):
    """
    Custom validator for ensuring email validity.

    The email must meet the following criteria:
    - Must be a valid email format.
    - Maximum length: 254 characters (RFC 5321 standard).
    """
    companyManager = CompanyManager(db_dsn=db_dsn)
    EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

    def validate(self, value: str) -> str:
        """
        Validates the email format.

        :param value: The email string to be validated.
        :return: The email if valid.
        """
        self.check_maximum_length(value)
        self.check_valid_email_format(value)
        self.check_email_availability(value)

        return value

    def check_email_availability(self, value: str) -> None:
        """
        Checks if the email is already in use.

        :param value: The email string to be checked.
        :raises ValidationError: If the email is already registered.
        """
        if self.companyManager.company_exists(value):
            raise serializers.ValidationError("This email is already registered.")

    def check_maximum_length(self, value: str) -> None:
        """
        Checks if the email does not exceed 254 characters.

        :param value: The email string to be checked.
        :raises ValidationError: If the email is longer than 254 characters.
        """
        if len(value) > 254:
            raise serializers.ValidationError("Email must not exceed 254 characters.")

    def check_valid_email_format(self, value: str) -> None:
        """
        Checks if the email is in a valid format.

        :param value: The email string to be checked.
        :raises ValidationError: If the email format is invalid.
        """
        if not re.match(self.EMAIL_REGEX, value):
            raise serializers.ValidationError("Invalid email format.")
