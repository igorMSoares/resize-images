from PIL import Image, ImageOps, UnidentifiedImageError
import os
import re

from .resizer_logger import ResizerLogger
from .messages import Messages
from .validators import SIZE_VALIDATION_REGEX


class ImageResizer:
    total_files_resized = 0

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
        while not re.match(SIZE_VALIDATION_REGEX, input_value):
            print(error_message.format(input_value=input_value))

            if not try_again_message:
                try_again_message = input_message

            input_value = input(try_again_message)

        return int(input_value.strip('px'))

    @classmethod
    def resize_all(cls, images_dir, resized_dir, new_largest_dimension):
        """Iterates the images_dir applying new_largest_dimension to each image.
        Returns the number of resized files.

        If original image's size is smaller than new_largest_dimension, the
        image won't be resized and an info will be written to the log file.

        If a non image file is present in the images_dir, the file will be ignored
        and a warning will be written to the log file.
        """

        for file_name in os.listdir(images_dir):
            file_path = os.path.join(images_dir, file_name)

            if os.path.isfile(file_path) and not file_name == '.gitignore':
                try:
                    with Image.open(file_path) as image:
                        image = ImageOps.exif_transpose(
                            image)  # Maintains orientation

                        if new_largest_dimension > max(image.size):
                            ResizerLogger.write_log(
                                'info',
                                Messages.output("file_not_resized").format(
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

                            image.save(f'{resized_dir}/{file_name}')
                            cls.total_files_resized += 1

                except UnidentifiedImageError as error:
                    ResizerLogger.write_log('warning', Messages.output(
                        "non_image_error").format(error=error))
                    ResizerLogger.something_in_log()
