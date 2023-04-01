import argparse
import os
import sys

from .messages import Messages
from .resizer_logger import ResizerLogger
from .image_resizer import ImageResizer
from .config import Config

class Arguments:
    default_args = Config.default_args()
    args = {
        'language': '',
        'encoding': '',
        'images_dir': '',
        'resized_dir': '',
        'log_file': '',
        'size': ''
    }

    IMAGES_DIR_FLAG = '--images_dir'
    RESIZED_DIR_FLAG = '--resized_dir'

    @classmethod
    def get_arguments(cls):
        parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            description='''
                        Resizes all images in a given directory (./imgs/ by default)
                        with a new largest dimension size, preserving the aspect ratio
                        and orientation of the images.
                        Can not be used to enlarge images.''')

        parser.add_argument('-d', cls.IMAGES_DIR_FLAG,
                            help='Directory with images to resize',
                            default=cls.default_args['images_dir'])
        parser.add_argument('-r', cls.RESIZED_DIR_FLAG,
                            help='Resized images directory',
                            default=cls.default_args['resized_dir'])
        parser.add_argument('-l', '--language',
                            help='Language of the output messages in ll_LL format',
                            default=cls.default_args['language'])
        parser.add_argument('-e', '--encoding',
                            help='Output messages encoding',
                            default=cls.default_args['encoding'])
        parser.add_argument('-f', '--log_file',
                            help='Name of the log file (specify full path if needed)',
                            default=cls.default_args['log_file'])
        parser.add_argument('-s', '--size',
                            help='Size, in pixels, of the largest dimension',
                            default=cls.default_args['size'])
        arguments = parser.parse_args()

        for key, _ in cls.args.items():
            cls.args[key] = getattr(arguments, key)

    @classmethod
    def get_args_passed_by_user(cls):
        return [key for key in cls.args.keys() if cls.args[key] != cls.default_args[key]]

    @classmethod
    def validate_argument(cls, arg):
        """Validates arguments passed in the command line"""

        def write_to_log_and_terminal(msg, level = 'error'):
            print(msg);
            ResizerLogger.write_log(level, msg)

        def language_validator():
            try:
                Messages.validate_language(cls.args["language"])
            except ValueError as error:
                default_lang = cls.default_args["language"]
                error_message = f'{error}{Messages.output("default_lang_error_msg").format(default_lang = default_lang)}'

                write_to_log_and_terminal(error_message, 'warning');

                cls.args["language"] = cls.default_args["language"]

        def images_dir_validator():
            try:
                ImageResizer.validate_directory(cls.args["images_dir"])
            except FileNotFoundError as error:
                error_message = (f'{error}{Messages.output("enter_dir_again").format(main_file_name = os.path.basename(sys.argv[0]), dir_flag = cls.IMAGES_DIR_FLAG)}')
                write_to_log_and_terminal(error_message)
                sys.exit(1);

        def resized_dir_validator():
            try:
                ImageResizer.validate_directory(cls.args["resized_dir"])
            except FileNotFoundError as error:
                error_message = (f'{error}{Messages.output("enter_dir_again").format(main_file_name = os.path.basename(sys.argv[0]), dir_flag = cls.RESIZED_DIR_FLAG)}')
                write_to_log_and_terminal(error_message)
                sys.exit(1)

        def encoding_validator():
            try:
                Messages.validate_encoding(cls.args["encoding"])
            except ValueError as error:
                default_encoding = cls.default_args["encoding"]
                error_message = f'{error}{Messages.output("default_enc_error_msg").format(default_encoding = default_encoding)}'

                write_to_log_and_terminal(error_message, 'warning')
                cls.args["encoding"] = default_encoding

        def log_file_validator():
            try:
                ResizerLogger.validate(cls.args["log_file"])
            except FileNotFoundError as error:
                default_log = cls.default_args["log_file"]
                error_message = f'{error}{Messages.output("default_log_error_msg").format(default_log = default_log)}'

                write_to_log_and_terminal(error_message, 'warning')
                cls.args["log_file"] = default_log

        def size_validator():
            if cls.args["size"]:
                try:
                    ImageResizer.validate_size(cls.args["size"])
                except ValueError as error:
                    write_to_log_and_terminal(error)
                    sys.exit(1);

        validate = {
            'language': language_validator,
            'images_dir': images_dir_validator,
            'resized_dir': resized_dir_validator,
            'encoding': encoding_validator,
            'log_file': log_file_validator,
            'size': size_validator,
        }

        validate[arg]();

    @classmethod
    def validate_user_args(cls, user_args):
        for arg in user_args:
            cls.validate_argument(arg)

    @classmethod
    def validate(cls):
        user_args = cls.get_args_passed_by_user()
        cls.validate_user_args(user_args)
