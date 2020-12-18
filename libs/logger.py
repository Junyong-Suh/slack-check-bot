import logging


# debug only goes to STDOUT
def debug(msg):
    logging.debug(msg)


def info(msg):
    logging.info(msg)


def error(msg):
    logging.error(msg)


def warning(msg):
    logging.warning(msg)
