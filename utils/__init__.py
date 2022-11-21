from utils.logger import Logger


logger = Logger()


def log_exceptions(func):
    def wrapper(self, *args, **kargs):
        try:
            return func(self, *args, **kargs)
        except Exception as ex:
            logger.error(f"error in '{func.__name__}' function -> {type(ex).__name__}{ex}")
    return wrapper
