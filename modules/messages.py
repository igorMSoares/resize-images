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
        if Messages.validate_language(lang) and Messages.validate_encoding(encoding):
            Messages.language = lang
            Messages.encoding = encoding

    @classmethod
    def validate_language(cls, language):
        if language not in Messages.available_languages():
            raise ValueError(Messages.output("invalid_language_error")
                                .format(language = language))
        else:
            return True

    @classmethod
    def validate_encoding(cls, encoding):
        try:
            codecs.lookup(encoding)
        except LookupError:
            raise ValueError(Messages.output("invalid_encoding_error")
                                .format(encoding = encoding))
        else:
            return True

    @classmethod
    def translated_messages(cls) -> dict:
        language_file = f'{Messages.languages_dir}/{Messages.language}.json'
        with open(language_file, "r", encoding=Messages.encoding) as json_file:
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
