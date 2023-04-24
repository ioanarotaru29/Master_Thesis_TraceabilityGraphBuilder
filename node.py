import fnmatch
import re
from enum import Enum
from pathlib import Path

from gherkin.parser import Parser as GherkinParser
from gherkin.token_scanner import TokenScanner
import javalang.parse as JavaParser


class Type(Enum):
    FEATURE = 'feature'
    TEST = 'test'
    CODE = 'code'

class Node:

    def __init__(self, location):
        self.__location = location

        if re.search(r'\.feature$', self.__location):
            self.type = Type.FEATURE

            parser = GherkinParser()
            parsed = parser.parse(TokenScanner(self.__location))
            print(parsed)

        elif re.search(r'/src/test/', self.__location):
            self.type = Type.TEST
            with open(self.__location, 'r') as file:
                parsed = JavaParser.parse(''.join(file.readlines()))
                print(parsed)
        else:
            self.type = Type.CODE
        self.fileName = Path(location).name


    def isFeature(self):
        return self.type == Type.FEATURE

    def isTest(self):
        return self.type == Type.TEST

    def isCode(self):
        return self.type == Type.CODE