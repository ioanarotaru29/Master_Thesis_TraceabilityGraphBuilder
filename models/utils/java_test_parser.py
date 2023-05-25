import inspect

import javalang
import javalang.parse as Parser
from javalang.tree import ClassCreator, MethodDeclaration

from models.node import Node


class JavaTestParser:
    def __init__(self, location):
        self.__location = location
        self.__name = ''
        self.__keywords = []
        self.__annotatated_keywords = {}

        all_classes = inspect.getmembers(javalang.tree, inspect.isclass)
        self.__allowed_classes = tuple(map(lambda x: x[1], filter(lambda x: x[0].find('Creator'), all_classes)))

    def parse(self):
        with open(self.__location, 'r') as file:
            try:
                parsed = Parser.parse(''.join(file.readlines()))
                types = getattr(parsed, 'types', [])
                for java_type in types:
                    self.__parse_type(java_type)
                return Node('TEST_CASE',
                            self.__location,
                            self.__name,
                            [],
                            self.__keywords + list(self.__annotatated_keywords.values())
                            ), self.__keywords, self.__annotatated_keywords
            except javalang.parser.JavaSyntaxError:
                print(self.__location)
        return None

    def __parse_type(self, java_type):
        self.__name = java_type.name
        self.__keywords.append(java_type.name)

        body = java_type.body
        if isinstance(body, (list, set, tuple)):
            for expression in list(body):
                self.__parse_body_expression(expression)
        else:
            self.__parse_body_expression(body)

    def __parse_body_expression(self, expression):
        if isinstance(expression, MethodDeclaration):
            try:
                annotations = getattr(expression, "annotations")
                annotated_element = getattr(annotations[0], "element")
                value = getattr(annotated_element, "value")
            except:
                value = None
            if value is not None:
                if value not in self.__annotatated_keywords.keys():
                    self.__annotatated_keywords[value] = []
                self.__parse_expression(expression, useAnnotated=value)
            else:
                self.__parse_expression(expression)
        else:
            self.__parse_expression(expression)

    def __parse_expression(self, expression, useAnnotated=None):
        accumulator = []
        attributes = getattr(expression, 'attrs', [])
        for attr in attributes:
            crt_obj = getattr(expression, attr)

            if attr == 'name' or attr == 'member':
                accumulator.append(crt_obj)
            elif isinstance(crt_obj, (list, set, tuple)):
                for obj in list(crt_obj):
                    if isinstance(obj, self.__allowed_classes):
                        self.__parse_expression(obj, useAnnotated)
            elif isinstance(crt_obj, self.__allowed_classes):
                self.__parse_expression(crt_obj, useAnnotated)
        if useAnnotated is None:
            self.__keywords += accumulator
        else:
            self.__annotatated_keywords[useAnnotated] += accumulator
