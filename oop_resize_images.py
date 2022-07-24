from PIL import Image, ImageOps

import os
from pathlib import Path

import re
import json
import logging
import argparse
import codecs


class Messages:
    languages_dir = './language'
    language = 'pt_BR'
    encoding = 'utf-8'

    @classmethod
    def set_language(cls, params):
        """
        @type params: dict
            {language = '',
            encoding = ''}
        """
        Messages.language = params['language']
        Messages.encoding = params['encoding']

    @classmethod
    def translated_messages(cls) -> dict:
        with open(Messages.languages_dir + "/" + Messages.language + ".json", "r", encoding=Messages.encoding) as json_file:
            return json.load(json_file)

    @classmethod
    def available_languages(cls):
        """Iterates languages_dir and returns an array with all the
        languages available (E.g.: ['pt_BR', 'en_US', 'es_AR'])"""

        json_files_path = list(Path(Messages.languages_dir).glob('*.json'))

        # Removes '.json' from file names
        json_files: list[str]
        json_files = list(map(lambda p: p.stem, json_files_path))

        # Remove all (if any) json files that are not in 'll_LL' format
        regex = re.compile('^[a-z]{2}_[A-Z]{2}')
        return [lang for lang in json_files if regex.match(lang)]

    @classmethod
    def output(cls, message, singular_or_plural=""):
        if singular_or_plural:
            return Messages.translated_messages()[message][singular_or_plural]
        else:
            return Messages.translated_messages()[message]


class ResizerLogger:
    log_has_something = False

    def __init__(self, date_format, log_file='log.txt', encoding='utf-8'):
        self.log_file = log_file
        self.encoding = encoding

        logging.basicConfig(
            filename=log_file,
            filemode='w',
            encoding=encoding,
            level=logging.INFO,
            format='%(asctime)s\n%(levelname)s: %(message)s\n',
            datefmt=date_format)

    @classmethod
    def something_in_log(cls):
        if not ResizerLogger.log_has_something:
            ResizerLogger.log_has_something = True

    @classmethod
    def write_log(cls, level, message):
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
        return [a for a in Arguments.default_args.keys() if Arguments.args[a] != Arguments.default_args.get(a)]

    @classmethod
    def validate_argument(cls, arg):
        """Validates argument passed in the command line"""

        match arg:
            case 'language':
                languages = Messages.available_languages()
                if Arguments.args["language"] not in languages:
                    print(f'"{Arguments.args["language"]}" is not available in {Messages.languages_dir}.\n' \
                          'Language will be set to "en_US".\n')
                    Arguments.args["language"] = 'en_US'
            case 'images_dir':
                if not os.path.isdir(Arguments.args["images_dir"]):
                    print(f'"{Arguments.args["images_dir"]}" is not a valid directory.\n' \
                          f'Run {os.path.basename(__file__)} again and use --image_dir ' \
                          'to specify a valid directory.')
                    exit()
            case 'resized_dir':
                if not os.path.isdir(Arguments.args["resized_dir"]):
                    print(f'"{Arguments.args["resized_dir"]}" is not a valid directory.\n' \
                          f'Run {os.path.basename(__file__)} again and use --resized_dir ' \
                          'to specify a valid directory.')
                    exit()
            case 'encoding':
                try:
                    codecs.lookup(Arguments.args["encoding"])
                except LookupError as error:
                    print(f'{error}. Using utf-8 instead.\n')
                    Arguments.args["encoding"] = 'utf-8'
            case 'log_file':
                if not Path(os.path.dirname(Arguments.args["log_file"])).exists():
                    print(f'"{Arguments.args["log_file"]}" is not a valid path. ' \
                          'Using "./log.txt" for log file instead.\n')
                    Arguments.args["log_file"] = 'log.txt'

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
    def get_largest_dimension(cls, input_message, error_message, try_again_message=""):
        """Asks user to enter the size of the resized image's largest dimension.

        If the input value is valid, returns the input value converted to an integer
        If not, shows error_message and
        asks for a different value, using try_again_message

        You may use '{input_value}' inside your error_message,
        and it will be replaced by the actual input_value entered by the user
        """

        input_value = input(input_message)

        while not re.match(r'^\d+\s?(px)?$', input_value):
            # Examples of valid inputs: '1200', '1200px' or '1200 px'
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
                            )
                            )
                            ResizerLogger.something_in_log()
                        else:
                            # Resizes image and maintains the aspect ratio
                            image.thumbnail((
                                new_largest_dimension,
                                new_largest_dimension))

                            image.save(f'{Arguments.args["resized_images_dir"]}/{file_name}')
                            ResizeImages.total_files_resized += 1

                except Image.UnidentifiedImageError as error:
                    ResizerLogger.write_log('warning', Messages.output("non_image_error").format(error=error))
                    ResizerLogger.something_in_log()


Arguments.get_arguments()
Arguments.validate()

logger = ResizerLogger(Messages.output("date_format"))

Messages.set_language({
    'language': Arguments.args['language'],
    'encoding': Arguments.args['encoding']
})

new_largest_dimension = ResizeImages.get_largest_dimension(
                            Messages.output('enter_data'),
                            Messages.output('invalid_data_error'),
                            Messages.output('enter_data_again'))
ResizeImages.resize_all(Arguments.args["images_dir"], new_largest_dimension)

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
