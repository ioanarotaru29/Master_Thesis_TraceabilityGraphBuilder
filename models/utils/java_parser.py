class JavaParser:
    def __init__(self, location):
        self.__location = location
        self.__name = ''
        self.__keywords = []

    def parse(self):
        return self.__name, self.__keywords
