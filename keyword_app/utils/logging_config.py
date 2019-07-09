import logging
import os

def setup_custom_logger(name):
    formatter = logging.Formatter(fmt='[%(asctime)s - %(filename)s:%(lineno)s - %(levelname)s - %(funcName)1s()]: %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, os.getenv('LOG_LEVEL', 'DEBUG').upper()))
    logger.addHandler(handler)
    return logger

if __name__  == '__main__':
    logger = setup_custom_logger('root')
    logger.info('Test logger')
    logger.warning('WARNING')
