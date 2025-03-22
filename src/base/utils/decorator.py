import functools
import logging
import time

from ..config import ENV

logger = logging.getLogger(ENV.app_name)

"""
import functools

def decorator(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        # Do something before
        value = func(*args, **kwargs)
        # Do something after
        return value
    return wrapper_decorator
"""


def perf(prefix: str = ""):
    """
    함수 실행 시간을 측정하는 데코레이터.

    :param prefix: 로그에 추가할 접두사
    """

    def __pass_args__(func):
        @functools.wraps(func)
        def __impl__(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            runtime = end_time - start_time

            location = f"{prefix}:{func.__name__}" if prefix else func.__name__
            logger.debug(f"{location} - {runtime * 1_000:.3f} ms")

            return result

        return __impl__

    return __pass_args__
