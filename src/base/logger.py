import sys
import logging.handlers
from base.config import settings

log = settings.app.logger
if log.level == "DEBUG":
    formatter = logging.Formatter("%(asctime)s[%(levelname)-8s] %(filename)s-%(lineno)s: %(message)s")
else:
    formatter = logging.Formatter("%(asctime)s[%(levelname)-8s] %(message)s")

root_logger = logging.getLogger(settings.app.name)
root_logger.setLevel(log.level)
root_logger.propagate = False


# Note. Stream Handler
streamHandler = logging.StreamHandler(sys.stdout)
streamHandler.setFormatter(formatter)
root_logger.addHandler(streamHandler)

# Note. File Handler
# fileHandler = logging.FileHandler(output_file)
# fileHandler.setFormatter(formatter)
# root_logger.addHandler(fileHandler)

# Note. Timed Rotating File Handler
timedHandler = logging.handlers.TimedRotatingFileHandler(
    log.dir.joinpath(f"{settings.app.name}.log"), when="midnight", interval=1, encoding="UTF-8", utc=False
)
timedHandler.setFormatter(formatter)
timedHandler.suffix = "%Y%m%d"  # 확인할 것.
root_logger.addHandler(timedHandler)
