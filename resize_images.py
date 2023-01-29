from PIL import Image, ImageOps, UnidentifiedImageError

import os
from pathlib import Path

import re
import logging
import argparse

from Messages import Messages

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
            print(f'[{error}] Using "log.txt" instead')
            ResizerLogger.log_file = 'log.txt'

    @classmethod
    def validate(cls, log_file):
        if not Path(os.path.dirname(Arguments.args["log_file"])).exists():
            raise FileNotFoundError(f'"{log_file}" is not a valid path. ')

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
                        Can't be used to enlarge images.''')

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

        for key, value in Arguments.args.items():
            Arguments.args[key] = getattr(arguments, key)

    @classmethod
    def get_args_passed_by_user(cls):
        return [key for key in Arguments.args.keys() if Arguments.args[key] != Arguments.default_args[key]]

    @classmethod
    def validate_argument(cls, arg):
        """Validates arguments passed in the command line"""

        def language_validator():
            try:
                Messages.validate_language(Arguments.args["language"])
            except ValueError as error:
                print(f'{error}\nLanguage will be set to "en_US".\n')
                Arguments.args["language"] = 'en_US'

        def images_dir_validator():
            try:
                ResizeImages.validate_directory(Arguments.args["images_dir"])
            except FileNotFoundError as error:
                exit(f'{error}\nRun {os.path.basename(__file__)} again '
                        'and use --image_dir ' 'to specify a valid directory.')

        def resized_dir_validator():
            try:
                ResizeImages.validate_directory(Arguments.args["resized_dir"])
            except FileNotFoundError as error:
                exit(f'{error}\nRun {os.path.basename(__file__)} again '
                        'and use --resized_dir to specify a valid directory.')

        def encoding_validator():
            try:
                Messages.validate_encoding(Arguments.args["encoding"])
            except LookupError as error:
                print(f'{error}. Using utf-8 instead.\n')
                Arguments.args["encoding"] = 'utf-8'

        def log_file_validator():
            try:
                ResizerLogger.validate(Arguments.args["log_file"])
            except FileNotFoundError as error:
                print(f'{error}\nUsing "./log.txt" for log file instead.\n')
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


class ResizeImages:
    total_files_resized = 0

    @classmethod
    def validate_directory(cls, directory):
        if not os.path.isdir(directory):
            raise FileNotFoundError(f'"{directory}" is not a valid directory.')

    @classmethod
    def get_largest_dimension(cls, input_message, error_message, try_again_message=""):
        """Asks user to enter the size of the resized image's largest dimension.

        If the input value is valid, returns the input value converted to an integer
        If not, shows error_message and
        asks for a different value, using try_again_message

        You may use '{input_value}' inside your error_message,
        and it will be replaced by the actual input_value entered by the user

        Examples of valid inputs: '1200', '1200px' or '1200 px'
        """

        input_value = input(input_message)
        while not re.match(r'^\d+\s?(px)?$', input_value):
            print(error_message.format(input_value=input_value))

            if not try_again_message:
                try_again_message = input_message

            input_value = input(try_again_message)
        else:
            return int(input_value.strip('px'))

    @classmethod
    def resize_all(cls, images_dir, new_largest_dimension):
        """Iterates the images_dir applying new_largest_dimension to each image.
        Returns the number of resized files.

        If original image's size is smaller than new_largest_dimension, the
        image won't be resized and an info will be written to the log file.

        If a non image file is present in the images_dir, the file will be ignored
        and a warning will be written to the log file.
        """

        for file_name in os.listdir(images_dir):
            file_path = f'{images_dir}/{file_name}'

            if os.path.isfile(file_path) and not file_name == '.gitignore':
                try:
                    with Image.open(file_path) as image:
                        image = ImageOps.exif_transpose(image)  # Maintains orientation

                        if new_largest_dimension > max(image.size):
                            ResizerLogger.write_log('info', Messages.output("file_not_resized").format(
                                file_name=file_name,
                                new_largest_dimension=new_largest_dimension,
                                img_width=image.width,
                                img_height=image.height
                            ))
                            ResizerLogger.something_in_log()
                        else:
                            # Resizes image and maintains the aspect ratio
                            image.thumbnail((
                                new_largest_dimension,
                                new_largest_dimension))

                            image.save(f'{Arguments.args["resized_dir"]}/{file_name}')
                            ResizeImages.total_files_resized += 1

                except UnidentifiedImageError as error:
                    ResizerLogger.write_log('warning', Messages.output("non_image_error").format(error=error))
                    ResizerLogger.something_in_log()


Arguments.get_arguments()
Arguments.validate()

ResizerLogger.init(Arguments.args['log_file'])

Messages.set_language(Arguments.args['language'])

new_dimension = ResizeImages.get_largest_dimension(
                    Messages.output('enter_data'),
                    Messages.output('invalid_data_error'),
                    Messages.output('enter_data_again'))
ResizeImages.resize_all(Arguments.args["images_dir"], new_dimension)

total = ResizeImages.total_files_resized
if total == 1:
    final_message = Messages.output("final_message", "singular")
    final_message += Messages.output("saved_to", "singular")
else:
    final_message = Messages.output("final_message", "plural")
    if total > 1:
        final_message += Messages.output("saved_to", "plural")

print(final_message.format(
    total_files_resized=total,
    resized_images_dir=Arguments.args["resized_dir"]
))

if ResizerLogger.log_has_something:
    print(Messages.output("check_the_log").format(log_file=Arguments.args["log_file"]))
