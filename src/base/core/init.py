import logging

from ..config import ENV
from ..constants import Color
from ..models import FallbackORM, UserORM
from ..utils import DBManager
from ..utils.common import get_password_hash

logger = logging.getLogger(ENV.app_name)


def init_admin():
    with DBManager() as manager:
        admin = manager.session.query(UserORM).filter(UserORM.username == "admin").all()
        if not admin:
            item = UserORM(username="admin", password=get_password_hash("admin"))
            _ = manager.insert(items=item)
            logger.debug(f"{Color.ORANGE}init admin ({item}){Color.DEFAULT}")


def init_db():
    with DBManager() as manager:
        manager.create_table(UserORM)
        manager.create_table(FallbackORM)
        logger.debug(f"{Color.ORANGE}{manager.init_log()}{Color.DEFAULT}")


class Initializer:
    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        init_db()
        init_admin()
