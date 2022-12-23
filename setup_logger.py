import logging

"""
https://docs.python.org/3/howto/logging.html#:~:text=logging.basicconfig(format%3D'%25(levelname)s%3A%25(message)s'%2C%20level%3Dlogging.debug)
"""

FILE_NAME = "log.txt"


def configer_logger(level=logging.ERROR):
    logging.basicConfig(
        format="%(levelname)s: %(message)s", level=level
    )  # , filename=FILE_NAME)
    logging.info("setup logger")
