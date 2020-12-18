import logging


logger = logging.getLogger("general")
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


# debug only goes to STDOUT
def debug(msg):
    logger.debug(msg)


def info(msg):
    logger.info(msg)


def error(msg):
    logger.error(msg)


def warning(msg):
    logger.warning(msg)
