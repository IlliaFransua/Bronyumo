from rest_framework import serializers

from .BaseValidator import BaseValidator


class PasswordStrengthValidator(BaseValidator):
    """
    Custom validator for ensuring password strength.

    Password must meet the following criteria:
    - Minimum length: 8 characters.
    - Maximum length: 64 characters.
    - Must contain at least one digit (0-9).
    - Must contain at least one uppercase letter (A-Z).
    - Must contain at least one lowercase letter (a-z).
    - Must contain at least one special character from the set (!@#$%^&*()-_=+[]{}|;:'",.<>?/).
    """

    def validate(self, value: str) -> str:
        """
        Validates the password strength based on various criteria.

        :param value: The password string to be validated.
        :return: The password if all criteria are met.
        """
        self.check_minimum_length(value)
        self.check_maximum_length(value)
        self.check_contains_digit(value)
        self.check_contains_uppercase(value)
        self.check_contains_lowercase(value)
        self.check_contains_special_character(value)

        return value

    def check_minimum_length(self, value: str) -> None:
        """
        Checks if the password has at least 8 characters.

        :param value: The password string to be checked.
        :raises ValidationError: If the password is shorter than 8 characters.
        """
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")

    def check_maximum_length(self, value: str) -> None:
        """
        Checks if the password does not exceed 64 characters.

        :param value: The password string to be checked.
        :raises ValidationError: If the password is longer than 64 characters.
        """
        if len(value) > 64:
            raise serializers.ValidationError("Password must not exceed 64 characters.")

    def check_contains_digit(self, value: str) -> None:
        """
        Checks if the password contains at least one digit (0-9).

        :param value: The password string to be checked.
        :raises ValidationError: If the password does not contain any digits.
        """
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Password must contain at least one digit.")

    def check_contains_uppercase(self, value: str) -> None:
        """
        Checks if the password contains at least one uppercase letter (A-Z).

        :param value: The password string to be checked.
        :raises ValidationError: If the password does not contain any uppercase letters.
        """
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")

    def check_contains_lowercase(self, value: str) -> None:
        """
        Checks if the password contains at least one lowercase letter (a-z).

        :param value: The password string to be checked.
        :raises ValidationError: If the password does not contain any lowercase letters.
        """
        if not any(char.islower() for char in value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")

    def check_contains_special_character(self, value: str) -> None:
        """
        Checks if the password contains at least one special character.

        :param value: The password string to be checked.
        :raises ValidationError: If the password does not contain any special characters.
        """
        special_characters = "!@#$%^&*()-_=+[]{}|;:'\",.<>?/"
        if not any(char in special_characters for char in value):
            raise serializers.ValidationError("Password must contain at least one special character.")
