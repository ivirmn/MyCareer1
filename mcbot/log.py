import logging
import os
from datetime import timedelta, datetime

def setup_logger(logger_name, log_file='bot.log'):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)

    log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(log_format)

    logger.addHandler(file_handler)
    return logger

def delete_old_logs(log_file='bot.log'):
    log_file_age = timedelta(weeks=2)
    if os.path.exists(log_file):
        file_modified_time = datetime.fromtimestamp(os.path.getmtime(log_file))
        if datetime.now() - file_modified_time > log_file_age:
            os.remove(log_file)