import logging
from typing import Optional

from ..config import ENV
from ..constants import Color
from ..models import FallbackORM
from ..models.exception import Fallback
from ..models.type import FallbackType
from ..utils import DBManager

logger = logging.getLogger(ENV.app_name)


class FallbackProcessor:
    def __init__(self):
        self.route = {
            FallbackType.INIT_FAIL: self.handle_fallback,
            FallbackType.FINAL_FAIL: self.handle_fallback,
            FallbackType.PLUGIN_LOAD_FAIL: self.handle_fallback,
            FallbackType.SOCK_CONN_FAIL: self.handle_fallback,
            FallbackType.REQUEST_FAIL: self.handle_fallback,
            FallbackType.TRANSACTION_FAIL: self.handle_fallback,
            FallbackType.VALID_DATA_FAIL: self.handle_fallback,
            FallbackType.UNDEFINED_FAIL: self.handle_fallback,
        }

    def __call__(self, *args, **kwargs):
        debug = kwargs.get("debug", True)
        fallback = kwargs.get("fallback", None)
        data = kwargs.get("data", None)

        self.dump_message_db(fallback=fallback, data=data)

        if debug:
            logger.debug(f"{Color.ORANGE}inner_function: {fallback.inner_function}{Color.DEFAULT}")

        handler = self.route.get(fallback.type)
        if handler:
            handler(fallback=fallback)

    @staticmethod
    def dump_message_db(fallback: Fallback, data: Optional[object] = None):
        with DBManager() as manager:
            item = FallbackORM(fallback=fallback, data=data)
            manager.insert(items=item)

    @staticmethod
    def handle_fallback(fallback: Fallback) -> None:
        """Handle different types of fallbacks with common logging."""
        logger.error(f"{Color.RED}{fallback.type}::{fallback.traceback}{Color.DEFAULT}")


fallback_processor = FallbackProcessor()
