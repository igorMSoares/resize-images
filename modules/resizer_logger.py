import logging
import os
from pathlib import Path

from .messages import Messages

class ResizerLogger:
    log_has_something = False
    log_file = ''

    @classmethod
    def init(cls, log_file='log.txt'):
        try:
            ResizerLogger.validate(log_file)
            ResizerLogger.log_file = log_file

            logging.basicConfig(
                filename=ResizerLogger.log_file,
                filemode='w',
                encoding=Messages.encoding,
                level=logging.INFO,
                format='%(asctime)s\n%(levelname)s: %(message)s\n',
                datefmt=Messages.output("date_format"))
        except FileNotFoundError as error:
            error_message = f'[{error}] Using "log.txt" instead'

            ResizerLogger.log_file = 'log.txt'

            print(error_message)
            ResizerLogger.write_log('warning', error_message)

    @classmethod
    def validate(cls, log_file):
        if not Path(os.path.dirname(log_file)).exists():
            raise FileNotFoundError(Messages.output("invalid_log_file_error").
                                        format(log_path = log_file))

    @classmethod
    def something_in_log(cls):
        if not ResizerLogger.log_has_something:
            ResizerLogger.log_has_something = True

    @classmethod
    def write_log(cls, level, message):
        if not ResizerLogger.log_file:
            ResizerLogger.init()
        log = getattr(logging, level)
        log(message)
