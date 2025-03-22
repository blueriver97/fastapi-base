import datetime
import traceback
from typing import Any, Dict

from pydantic import BaseModel

from ..utils.common import convert_datetime_to_timestamp, uuid4
from .exception import Fallback
from .type import FallbackType


class Message(BaseModel):
    data: Dict[str, Any]

    __annotations__ = {
        "data": Dict[str, Any],
    }

    def value_validation(self):
        try:
            assert self.data is not None, "Message.data is no value."
        except Exception:
            raise Fallback(type=FallbackType.VALID_DATA_FAIL, traceback=traceback.format_exc())

    def fill(self):
        self.id = uuid4().hex
        self.server_timestamp = convert_datetime_to_timestamp(datetime.datetime.now())
