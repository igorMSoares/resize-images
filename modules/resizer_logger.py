import logging

from .messages import Messages
from .validators import validate_log_file
from .config import Config

class ResizerLogger:
    validation_error = None
    log_has_something = False
    log_file = Config.default_args()['log_file']

    @classmethod
    def init(cls, log_file=log_file):
        if cls.validate(log_file):
            cls.log_file = log_file 
            
        logging.basicConfig(
            filename=cls.log_file,
            filemode='w',
            encoding=Messages.encoding,
            level=logging.INFO,
            format='%(asctime)s\n%(levelname)s: %(message)s\n',
            datefmt=Messages.output("date_format"))
        
        if cls.validation_error:
            error_msg = f'{cls.validation_error}{Messages.output("default_log_error_msg").format(default_log = cls.log_file)}'
            print(error_msg)
            cls.write_log('warning', error_msg)

    @classmethod
    def validate(cls, log_file):
        try:
            validate_log_file(log_file)
            return True
        except FileNotFoundError as error:
            cls.validation_error = error
            return False

    @classmethod
    def something_in_log(cls):
        if not cls.log_has_something:
            cls.log_has_something = True

    @classmethod
    def write_log(cls, level, message):
        if not cls.log_file:
            cls.init()
        log = getattr(logging, level)
        log(message)
