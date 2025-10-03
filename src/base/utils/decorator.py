import functools
import logging
import time

logger = logging.getLogger(__file__)


def perf(prefix: str = ""):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            runtime = end_time - start_time

            logger.debug(f"'{prefix}{func.__name__}' executed in {runtime * 1_000:.3f} ms")

            return result

        return wrapper

    return decorator


"""
@perf("API:")
def call_external_api():
    time.sleep(0.2)
    return {"status": "ok"}


call_external_api()
# 예상 로그: 'API:call_external_api' executed in 200.456 ms
"""
