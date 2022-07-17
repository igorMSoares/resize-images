from PIL import Image, ImageOps

import os
from os import listdir

import re # Regular Expressions Library
import json
import logging


def something_in_log():
    '''Sets True only the first time that something is written to log_file'''

    global log_has_something
    if not log_has_something:
        log_has_something = True


def set_largest_dimension(input_message, error_message, try_again_message=False):
    '''If the input value is valid, returns the input value converted to a integer
    If not, shows error_message and
    asks for a different value, using try_again_message

    You may use '<--input value-->' placeholder inside your error_message,
    and it will be replaced by the actual input_value entered by the user
    '''

    input_value = input(input_message)

    # Using Regular Expressions to test whether the input value is valid
    while not re.match('^\d+\s{0,1}(px){0,1}$', input_value):
        # input_value is not starting with one or more digits <^\d+>
        # followed by none or one white space <\s{0,1}>
        # and ending with one or none 'px' unit <(px){0,1}$>
        #
        # Examples of valid inputs: '1200', '1200px'ou '1200 px'
        print(error_message.replace('<--input value-->', input_value))

        if not try_again_message:
            # If a try_again_message is not passed to the function,
            # the input_message will be used again
            try_again_message = input_message

        input_value = input(try_again_message)
    else:
        return int(input_value.strip('px'))


# Initializing variables
language = 'pt_BR'
encoding = 'utf-8'
with open("language/"+language+".json", "r", encoding=encoding) as json_file:
    messages = json.load(json_file)

log_file = './log.txt'
logging.basicConfig(
            filename = log_file,
            filemode = 'w',
            encoding = encoding,
            level = logging.INFO,
            format = '%(asctime)s\n%(levelname)s: %(message)s\n',
            datefmt = messages["date_format"]) # datefmt in language file

# Indicates that something has been written to log_file
log_has_something = False

images_dir = './imgs'
resized_images_dir = f'{images_dir}/resized'
total_files_resized = 0

# Messages that will be displayed to the user
input_message = messages["enter_data"]

error_message = messages["invalid_data_error"]

try_again_message = messages["enter_data_again"]

new_largest_dimension = set_largest_dimension(
                            input_message,
                            error_message,
                            try_again_message)

for file_name in os.listdir(images_dir):
    file_path = f'{images_dir}/{file_name}'

    # Checks if it's not a directory and ignores .gitignore file
    if os.path.isfile(file_path) and not file_name=='.gitignore':
        try:
            with Image.open(file_path) as image: # Context Manager
                image = ImageOps.exif_transpose(image) # Maintains orientation

                if new_largest_dimension > max(image.size):
                    logging.info(messages["file_not_resized"].format(
                                    file_name=file_name,
                                    new_largest_dimension=new_largest_dimension,
                                    img_width=image.width,
                                    img_height=image.height
                                    )
                                )
                    something_in_log()
                else:
                    # Resizes image's largest dimension
                    # with new_largest_dimension and maintains the aspect ratio
                    image.thumbnail((
                            new_largest_dimension,
                            new_largest_dimension))

                    image.save(f'{resized_images_dir}/{file_name}')
                    total_files_resized += 1

        except Image.UnidentifiedImageError as error:
            # When Image.open() receives a non image file as argument
            logging.warning(messages["non_image_error"].format(error=error))
            something_in_log()

if total_files_resized == 1:
    final_message = messages["final_message"]["singular"]
    final_message += messages["saved_to"]["singular"]
else:
    final_message = messages["final_message"]["plural"]
    if total_files_resized > 0:
            final_message += messages["saved_to"]["plural"]


print(final_message.format(
            total_files_resized=total_files_resized,
            resized_images_dir=resized_images_dir
        ))

if log_has_something:
    print(messages["check_the_log"].format(log_file=log_file))
