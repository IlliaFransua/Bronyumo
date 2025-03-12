from abc import ABC, abstractmethod
from typing import Any


class BaseValidator(ABC):
    """
    Abstract base class for implementing custom validators.

    This class defines the basic structure for validators that check the validity of a given value.
    Any custom validator should inherit from this class and implement the `validate` method.
    """

    @abstractmethod
    def validate(self, value: Any) -> Any:
        """
        Abstract method that needs to be implemented by subclasses to perform validation.

        :param value: The value to be validated. The type of this value depends on the specific validator.
        :return: The validated value if the validation passes.
        :raises ValidationError: If the validation fails, an exception should be raised.
        """
        pass
