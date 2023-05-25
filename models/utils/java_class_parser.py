import inspect

import javalang
import javalang.parse as Parser
from javalang.tree import ClassCreator

from models.node import Node


class JavaClassParser:
    def __init__(self, location):
        self.__location = location
        self.__name = ''
        self.__keywords = []

        all_classes = inspect.getmembers(javalang.tree, inspect.isclass)
        self.__allowed_classes = tuple(map(lambda x: x[1], filter(lambda x: x[0].find('Creator'), all_classes)))

    def parse(self):
        with open(self.__location, 'r') as file:
            try:
                parsed = Parser.parse(''.join(file.readlines()))
                types = getattr(parsed, 'types', [])
                for java_type in types:
                    self.__parse_type(java_type)
                return Node('SOURCE_CODE', self.__location, self.__name, [], list(set(self.__keywords)))
            except javalang.parser.JavaSyntaxError:
                print(self.__location)
        return None

    def __parse_type(self, java_type):
        self.__name = java_type.name
        self.__keywords.append(java_type.name)

        extends = getattr(java_type, 'extends', [])
        if isinstance(extends, (list, set, tuple)):
            for expression in list(extends):
                self.__parse_expression(expression)
        else:
            self.__parse_expression(extends)
        implements = getattr(java_type, 'implements', [])
        if isinstance(implements, (list, set, tuple)):
            for expression in list(implements):
                self.__parse_expression(expression)
        else:
            self.__parse_expression(implements)

        body = java_type.body
        if isinstance(body, (list, set, tuple)):
            for expression in list(body):
                self.__parse_expression(expression)
        else:
            self.__parse_expression(body)

    def __parse_expression(self, expression):
        attributes = getattr(expression, 'attrs', [])
        for attr in attributes:
            crt_obj = getattr(expression, attr)

            if attr == 'name' or attr == 'member':
                self.__keywords.append(crt_obj)
            elif isinstance(crt_obj, (list, set, tuple)):
                for obj in list(crt_obj):
                    if isinstance(obj, self.__allowed_classes):
                        self.__parse_expression(obj)
            elif isinstance(crt_obj, self.__allowed_classes):
                self.__parse_expression(crt_obj)
