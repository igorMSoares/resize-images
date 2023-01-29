# This is the first implementation I did using a pure functional approach
# This version is no longer being maintened and I keep this file just for the record
# The current version (resize_images.py) uses a Class Oriented approach

from PIL import Image, ImageOps, UnidentifiedImageError

import os
from pathlib import Path

import re
import json
import logging
import argparse
import codecs


def set_largest_dimension(input_message, error_message, try_again_message=False):
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


def resize_images(images_directory, new_dimension):
    """Iterates the images_dir applying new_largest_dimension to each image.
    Returns the number of resized files.

    If original image's size is smaller than new_largest_dimension, the
    image won't be resized and an info will be written to the log file.

    If a non image file is present in the images_dir, the file will be ignored
    and a warning will be written to the log file.
    """
    total_files_resized = 0

    for file_name in os.listdir(images_directory):
        file_path = f'{images_directory}/{file_name}'

        if os.path.isfile(file_path) and not file_name == '.gitignore':
            try:
                with Image.open(file_path) as image:
                    image = ImageOps.exif_transpose(image)  # Maintains orientation

                    if new_dimension > max(image.size):
                        logging.info(messages["file_not_resized"].format(
                                        file_name=file_name,
                                        new_largest_dimension=new_dimension,
                                        img_width=image.width,
                                        img_height=image.height
                                        )
                                     )
                        something_in_log()
                    else:
                        # Resizes image and maintains the aspect ratio
                        image.thumbnail((
                            new_dimension,
                            new_dimension))

                        image.save(f'{resized_images_dir}/{file_name}')
                        total_files_resized += 1

            except UnidentifiedImageError as error:
                logging.warning(messages["non_image_error"].format(error=error))
                something_in_log()

    return total_files_resized


def get_languages(languages_directory):
    """Iterates languages_dir and returns an array with all the
    languages available (E.g.: ['pt_BR', 'en_US', 'es_AR'])"""

    json_files = list(Path(languages_directory).glob('*.json'))

    # Removes '.json' from file names
    json_files = list(map(lambda p: p.stem, json_files))

    # Remove all (if any) json files that are not in 'll_LL' format
    regex = re.compile('^[a-z]{2}_[A-Z]{2}')
    return [lang for lang in json_files if regex.match(lang)]


def get_all_args():
    """Gets all the arguments passed in the command line or assigns a default value"""

    parser = argparse.ArgumentParser(
                formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                description='''
                    Resizes all images in a given directory (./imgs/ by default)
                    with a new largest dimension size, preserving the aspect ratio
                    and orientation of the images.
                    Can't be used to enlarge images.''')

    parser.add_argument('-d', '--images_dir',
                            help='Directory with images to resize',
                            default=default_args['images_dir'])
    parser.add_argument('-r', '--resized_dir',
                            help='Resized images directory',
                            default=default_args['resized_dir'])
    parser.add_argument('-l', '--language',
                            help='Language of the output messages in ll_LL format',
                            default=default_args['language'])
    parser.add_argument('-e', '--encoding',
                            help='Output messages encoding',
                            default=default_args['encoding'])
    parser.add_argument('-f', '--log_file',
                            help='Name of the log file (specify full path if needed)',
                            default=default_args['log_file'])

    return parser.parse_args()


def get_args_passed_by_user(default_arguments):
    return [key for key in vars(args).keys() if vars(args)[key] != default_arguments[key]]


def validate_argument(arg):
    """Validates argument passed in the command line"""

    match arg:
        case 'language':
            languages = get_languages(languages_dir)
            if args.language not in languages:
                print(f'"{args.language}" is not available in {languages_dir}.\n'
                      'Language will be set to "en_US".\n')
                args.language = 'en_US'
        case 'images_dir':
            if not os.path.isdir(args.images_dir):
                print(f'"{args.images_dir}" is not a valid directory.\n'
                      f'Run {os.path.basename(__file__)} again and use --image_dir '
                      'to specify a valid directory.')
                exit()
        case 'resized_dir':
            if not os.path.isdir(args.resized_dir):
                print(f'"{args.resized_dir}" is not a valid directory.\n'
                      f'Run {os.path.basename(__file__)} again and use --resized_dir '
                      'to specify a valid directory.')
                exit()
        case 'encoding':
            try:
                codecs.lookup(args.encoding)
            except LookupError as error:
                print(f'{error}. Using utf-8 instead.\n')
                args.encoding = 'utf-8'
        case 'log_file':
            if not Path(os.path.dirname(args.log_file)).exists():
                print(f'"{args.log_file}" is not a valid path. '
                      'Using "./log.txt" for log file instead.\n')
                args.log_file = 'log.txt'


def validate_user_args(arguments):
    for arg in arguments:
        validate_argument(arg)


def something_in_log():
    """Sets True only the first time that something is written to log_file"""

    global log_has_something
    if not log_has_something:
        log_has_something = True


# Initializing variables
default_args = {
    'language': 'pt_BR',
    'encoding': 'utf-8',
    'images_dir': './imgs',
    'resized_dir': './imgs/resized',
    'log_file': 'log.txt'
}
languages_dir = './language'

args = get_all_args()
user_args = get_args_passed_by_user(default_args)
validate_user_args(user_args)

language = args.language
encoding = args.encoding
with open(languages_dir+"/"+language+".json", "r", encoding=encoding) as json_file:
    messages = json.load(json_file)

log_file = args.log_file
logging.basicConfig(
            filename=log_file,
            filemode='w',
            encoding=encoding,
            level=logging.INFO,
            format='%(asctime)s\n%(levelname)s: %(message)s\n',
            datefmt=messages["date_format"])  # datefmt in language file

log_has_something = False

images_dir = args.images_dir
resized_images_dir = args.resized_dir

new_largest_dimension = set_largest_dimension(
                            messages["enter_data"],
                            messages["invalid_data_error"],
                            messages["enter_data_again"])

total_images = resize_images(images_dir, new_largest_dimension)

if total_images == 1:
    final_message = messages["final_message"]["singular"]
    final_message += messages["saved_to"]["singular"]
else:
    final_message = messages["final_message"]["plural"]
    if total_images > 1:
        final_message += messages["saved_to"]["plural"]


print(final_message.format(
            total_files_resized=total_images,
            resized_images_dir=resized_images_dir
        ))

if log_has_something:
    print(messages["check_the_log"].format(log_file=log_file))
