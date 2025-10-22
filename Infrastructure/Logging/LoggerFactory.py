import logging

class LoggerFactory:
    @staticmethod
    def create_logger(name: str):
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        return logger
