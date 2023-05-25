import re
import xml.etree.ElementTree as et

from models.node import Node


class XmlResultsParser:
    def __init__(self, location):
        self.__location = location
        self.__durations = {}
        self.__faults = {}

    def parse(self):
        tree = et.parse(self.__location)
        root = tree.getroot()
        self.__parse_level(root)

        return self.__durations, self.__faults

    def __parse_level(self, parent):
        name = parent.get('name')
        for child in parent:
            if child.tag == 'suite' or child.tag == 'test':
                c_name = child.get('name')
                if re.search(name + '\.', c_name) is None:
                    c_name = name + '.' + c_name
                self.__durations[c_name] = child.get('duration')
            if child.tag == 'suite':
                self.__parse_level(child)