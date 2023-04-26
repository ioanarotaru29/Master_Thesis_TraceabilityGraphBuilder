from models.utils.gherkin_parser import GherkinParser
from models.utils.java_parser import JavaParser
from models.utils.text_sanitizer import TextSanitizer
import re


# def transform(word):
#     # Underline
#     new_word = word.replace('_', ' ')
#     # Camel Case
#     if not new_word.isupper():
#         new_word = ' '.join(re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', new_word))
#     return new_word.lower()


class Node:
    def __init__(self, file_location, file_type, sanitizer=None):
        self.__sanitizer = sanitizer or TextSanitizer()
        self.__location = file_location
        self.__type = file_type

        self.__parse()
        self.__sanitize()
        print(self.__name, self.__keywords)

    def __get_parser(self):
        if self.__type == 'FEATURE':
            return GherkinParser(self.__location)
        elif self.__type == 'TEST':
            return JavaParser(self.__location)
        elif self.__type == 'CODE':
            return JavaParser(self.__location)
        else:
            raise ValueError(self.__type)

    def __parse(self):
        parser = self.__get_parser()
        self.__name, self.__keywords = parser.parse()

    def __sanitize(self):
        sentence = ' '.join(self.__keywords)

        result = self.__sanitizer.sanitize(sentence,
                                           use_transform=self.__type != 'FEATURE',
                                           use_entity_recognition=self.__type == 'FEATURE')
        if result is not None:
            self.__keywords = result

    def type(self):
        return self.__type

    def keywords(self):
        return self.__keywords

    def name(self):
        return self.__name