import logging
import os
import sys

from .config import ENV

os.makedirs(ENV.log_dir, exist_ok=True)

if ENV.app_name:
    # Note. Default Settings
    app_logger = logging.getLogger(ENV.app_name)
    app_logger.setLevel(ENV.log_level)
    app_logger.propagate = False
    output_file: str = os.path.join(ENV.log_dir, ENV.log_file)

    if ENV.log_level == 10:
        formatter = logging.Formatter("%(asctime)s[%(levelname)-8s] %(filename)s-%(lineno)s: %(message)s")
    else:
        formatter = logging.Formatter("%(asctime)s[%(levelname)-8s] %(message)s")

    # Note. Stream Handler
    streamHandler = logging.StreamHandler(sys.stdout)
    streamHandler.setFormatter(formatter)
    app_logger.addHandler(streamHandler)

    # Note. File Handler
    fileHandler = logging.FileHandler(output_file)
    fileHandler.setFormatter(formatter)
    app_logger.addHandler(fileHandler)

    # Note. Timed Rotating File Handler
    # timedHandler = logging.handlers.TimedRotatingFileHandler(
    #     output_file,
    #     when="midnight", interval=1, encoding="UTF-8", utc=False
    # )
    # timedHandler.setFormatter(formatter)
    # timedHandler.suffix = "%Y%m%d"  # 확인할 것.
    # app_logger.addHandler(timedHandler)
