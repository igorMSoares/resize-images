import argparse
import os
import sys

from .messages import Messages
from .resizer_logger import ResizerLogger
from .image_resizer import ImageResizer

class Arguments:
    default_args = {
        'language': 'pt_BR',
        'encoding': 'utf-8',
        'images_dir': './imgs',
        'resized_dir': './imgs/resized',
        'log_file': 'log.txt'
    }
    args = {
        'language': '',
        'encoding': '',
        'images_dir': '',
        'resized_dir': '',
        'log_file': ''
    }

    @classmethod
    def get_arguments(cls):
        parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            description='''
                        Resizes all images in a given directory (./imgs/ by default)
                        with a new largest dimension size, preserving the aspect ratio
                        and orientation of the images.
                        Can not be used to enlarge images.''')

        parser.add_argument('-d', '--images_dir',
                            help='Directory with images to resize',
                            default=Arguments.default_args['images_dir'])
        parser.add_argument('-r', '--resized_dir',
                            help='Resized images directory',
                            default=Arguments.default_args['resized_dir'])
        parser.add_argument('-l', '--language',
                            help='Language of the output messages in ll_LL format',
                            default=Arguments.default_args['language'])
        parser.add_argument('-e', '--encoding',
                            help='Output messages encoding',
                            default=Arguments.default_args['encoding'])
        parser.add_argument('-f', '--log_file',
                            help='Name of the log file (specify full path if needed)',
                            default=Arguments.default_args['log_file'])
        arguments = parser.parse_args()

        for key, _ in Arguments.args.items():
            Arguments.args[key] = getattr(arguments, key)

    @classmethod
    def get_args_passed_by_user(cls):
        return [key for key in Arguments.args.keys() if Arguments.args[key] != Arguments.default_args[key]]

    @classmethod
    def validate_argument(cls, arg):
        """Validates arguments passed in the command line"""

        def write_to_log_and_terminal(msg, level = 'error'):
            print(msg);
            ResizerLogger.write_log(level, msg)

        def language_validator():
            try:
                Messages.validate_language(Arguments.args["language"])
            except ValueError as error:
                error_message = f'{error}\nLanguage will be set to "en_US".\n'

                write_to_log_and_terminal(error_message, 'warning');

                Arguments.args["language"] = 'en_US'

        def images_dir_validator():
            try:
                ImageResizer.validate_directory(Arguments.args["images_dir"])
            except FileNotFoundError as error:
                error_message = (f'{error}\nRun {os.path.basename(__file__)} again '
                        'and use --image_dir ' 'to specify a valid directory.')

                write_to_log_and_terminal(error_message)
                sys.exit(1);

        def resized_dir_validator():
            try:
                ImageResizer.validate_directory(Arguments.args["resized_dir"])
            except FileNotFoundError as error:
                error_message = (f'{error}\nRun {os.path.basename(__file__)} again '
                        'and use --resized_dir to specify a valid directory.')

                write_to_log_and_terminal(error_message)
                sys.exit(1)

        def encoding_validator():
            try:
                Messages.validate_encoding(Arguments.args["encoding"])
            except LookupError as error:
                error_message = f'{error}. Using utf-8 instead.\n'

                write_to_log_and_terminal(error_message, 'warning')
                Arguments.args["encoding"] = 'utf-8'

        def log_file_validator():
            try:
                ResizerLogger.validate(Arguments.args["log_file"])
            except FileNotFoundError as error:
                error_message = f'{error}\nUsing "./log.txt" for log file instead.\n'

                write_to_log_and_terminal(error_message, 'warning')
                Arguments.args["log_file"] = 'log.txt'

        validate = {
            'language': language_validator,
            'images_dir': images_dir_validator,
            'resized_dir': resized_dir_validator,
            'encoding': encoding_validator,
            'log_file': log_file_validator,
        }

        validate[arg]();

    @classmethod
    def validate_user_args(cls, user_args):
        for arg in user_args:
            Arguments.validate_argument(arg)

    @classmethod
    def validate(cls):
        user_args = Arguments.get_args_passed_by_user()
        Arguments.validate_user_args(user_args)
