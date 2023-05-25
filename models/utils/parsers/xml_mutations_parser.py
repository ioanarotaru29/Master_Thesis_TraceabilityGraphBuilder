import xml.etree.ElementTree as et

from models.node import Node


class XmlMutationsParser:
    def __init__(self, location):
        self.__location = location
        self.__faults = {}

    def parse(self):
        tree = et.parse(self.__location)
        root = tree.getroot()
        for mutation in root.iter("mutation"):
            if mutation.get("status") == "KILLED":
                text = mutation.find("killingTest").text or ''
                test_name = text.split('.')[-1]
                test_name = test_name.replace(' : ', '.')
                if test_name not in self.__faults.keys():
                    self.__faults[test_name] = []
                self.__faults[test_name].append(Node('FAULT', '', ''))

        return self.__faults