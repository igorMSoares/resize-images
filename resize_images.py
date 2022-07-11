from PIL import Image, ImageOps

import os
from os import listdir

import re # Regular Expressions Library

import logging

log_file = 'log.txt'
logging.basicConfig(
            filename = log_file,
            filemode = 'w',
            level = logging.INFO,
            format = '%(asctime)s\n%(levelname)s: %(message)s\n',
            datefmt = '%d/%b/%Y %H:%M:%S')

# Indicates that something has been written to log_file
log_has_something = False

def something_in_log():
    '''Sets True only the first time that something is written to log_file'''

    global log_has_something
    if not log_has_something:
        log_has_something = True


def singular_or_plural():
    '''Outputs final message in singular form if total_files_resized == 1'''

    global total_files_resized
    if total_files_resized == 1:
        return ""
    else:
        return "s"


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
images_dir = './imgs'
resized_images_dir = f'{images_dir}/resized'
total_files_resized = 0

# Messages that will be displayed to the user
input_message = 'Qual tamanho, em pixels, deverá ter o maior lado da imagem? ' \
                    '(A proporção será mantida)\n'

error_message = f'\n[ERRO] "<--input value-->" não é um número válido. ' \
                    'Tente novamente.\n'  # <--input value--> is a placeholder

try_again_message = 'Qual tamanho, em pixels, deverá ter o maior lado ' \
                        'da imagem? (Ex.: 1200px)\n'

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
                    logging.info(f'"{file_name}" não foi redimensionado.\n' \
                                    f'"{new_largest_dimension}px" é maior do ' \
                                    'que o tamanho original da imagem: ' \
                                    f'({image.width}px,{image.height}px)')
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
            logging.warning(f'{error} (não é um arquivo de imagem válido)\n')
            something_in_log()

final_message = f'\n{total_files_resized} arquivo{singular_or_plural()} ' \
                    f'redimensionado{singular_or_plural()}'

if total_files_resized > 0:
    final_message+=f' e salvo{singular_or_plural()} ' \
                        f'na pasta "{resized_images_dir}"'

print(final_message)
if log_has_something:
    print(f'Acesse o arquivo "./{log_file}" para mais informações')
