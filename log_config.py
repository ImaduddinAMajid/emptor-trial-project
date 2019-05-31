import logging
import sys

logger = logging.getLogger()
for h in logger.handlers:
    logger.removeHandler(h)
h = logging.StreamHandler(sys.stdout)

FORMAT = "%(asctime)-15s %(process)d-%(thread)d %(name)s [%(filename)s:%(lineno)d] :%(levelname)8s: %(message)s"
h.setFormatter(logging.Formatter(FORMAT))
logger.addHandler(h)
logger.setLevel(logging.DEBUG)

logging.getLogger("__main__").setLevel(logging.DEBUG)
logging.getLogger("botocore").setLevel(logging.WARN)
logging.getLogger("pynamodb").setLevel(logging.INFO)
