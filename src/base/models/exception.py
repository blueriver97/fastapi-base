import inspect
import logging
from typing import Optional

from ..config import ENV
from .type import FallbackType

logger = logging.getLogger(ENV.app_name)


class Fallback(Exception):
    """Custom exception to handle fallback scenarios."""

    def __init__(self, type: FallbackType, traceback: Optional[str] = None):
        """
        Initializes a Fallback exception.

        :param type: The type of fallback (FallbackType).
        :param traceback: The traceback string of the exception.
        :param inner_function: The name of the function where the exception occurred.
        """
        self.type = type
        self.traceback = traceback

        frame = inspect.currentframe()
        if frame is not None and frame.f_back is not None:
            self.inner_function = frame.f_back.f_code.co_name

        # self.inner_function = inspect.currentframe().f_back.f_code.co_name

    def __str__(self):
        """Return a formatted string representation of the exception."""
        return f"{self.__class__.__name__}<{self.type}>\n{self.traceback}"
