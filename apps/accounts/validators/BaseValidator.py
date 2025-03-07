from abc import ABC, abstractmethod

class BaseValidator(ABC):
    @abstractmethod
    def validate(self, value):
        """Checks the value and returns it if anything is ok or generates an error."""
        pass