import codecs
import json
import re
from pathlib import Path

from .config import Config

class Messages:
    languages_dir = './language'
    language = Config.default_args()["language"]
    encoding = Config.default_args()["encoding"]

    @classmethod
    def set_language(cls, lang, encoding='utf-8'):
        if cls.validate_language(lang) and cls.validate_encoding(encoding):
            cls.language = lang
            cls.encoding = encoding

    @classmethod
    def validate_language(cls, language):
        if language not in cls.available_languages():
            raise ValueError(cls.output("invalid_language_error")
                                .format(language = language))
        else:
            return True

    @classmethod
    def validate_encoding(cls, encoding):
        try:
            codecs.lookup(encoding)
        except LookupError:
            raise ValueError(cls.output("invalid_encoding_error")
                                .format(encoding = encoding))
        else:
            return True

    @classmethod
    def translated_messages(cls) -> dict:
        language_file = f'{cls.languages_dir}/{cls.language}.json'
        with open(language_file, "r", encoding=cls.encoding) as json_file:
            return json.load(json_file)

    @classmethod
    def available_languages(cls):
        """Iterates languages_dir and returns an array with all the
        languages available (E.g.: ['pt_BR', 'en_US', 'es_AR'])"""

        json_files_path = list(Path(cls.languages_dir).glob('*.json'))

        # Removes '.json' from file names
        json_files: list[str]
        json_files = list(map(lambda p: p.stem, json_files_path))

        # Remove all (if any) json files that are not in 'll_LL' format
        regex = re.compile('^[a-z]{2}_[A-Z]{2}')
        return [lang for lang in json_files if regex.match(lang)]

    @classmethod
    def output(cls, message, singular_or_plural=""):
        if singular_or_plural:
            return cls.translated_messages()[message][singular_or_plural]
        else:
            return cls.translated_messages()[message]
