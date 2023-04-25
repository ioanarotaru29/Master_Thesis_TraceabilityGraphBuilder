from models.utils.gherkin_parser import GherkinParser
from models.utils.java_parser import JavaParser


class Node:
    def __init__(self, file_location, file_type):
        self.__location = file_location
        self.__type = file_type

        parser = self.__get_parser()
        self.__name, self.__keywords = parser.parse()
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


