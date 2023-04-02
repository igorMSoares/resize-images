import os
import re
from pathlib import Path

from .messages import Messages


SIZE_VALIDATION_REGEX = r'^\d+\s?(px)?$'

def validate_directory(directory):
    if not os.path.isdir(directory):
        raise FileNotFoundError(
            Messages.output('invalid_dir_error')
            .format(directory = directory))

def validate_size(size):
    if not re.match(SIZE_VALIDATION_REGEX, size):
        raise ValueError(
            Messages.output('invalid_data_error')
            .format(input_value = size))

def validate_language(language):
  try:
    Messages.validate_language(language)
  except ValueError as error:
    raise ValueError(error)

def validate_encoding(encoding):
  try:
    Messages.validate_encoding(encoding)
  except ValueError as error:
    raise ValueError(error)

def validate_log_file(log_file):
  if not Path(os.path.dirname(log_file)).exists():
      raise FileNotFoundError(Messages.output("invalid_log_file_error").
                                  format(log_path = log_file))