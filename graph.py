import fnmatch
import os
import re
from pathlib import Path

from node import Node


class Graph:
    def __init__(self, location):
        self.__location = location
        self.__parse()

    def __parse(self):
        self.nodes = []

        includes = ['*.feature', '*.java']
        includes = r'|'.join([fnmatch.translate(x) for x in includes])
        for path, subdirs, files in os.walk(self.__location):
            for file in files:
                if re.match(includes, file):
                    node = Node(os.path.join(path, file))
                    self.nodes.append(node)

    def features(self):
        return list(filter(lambda node: node.isFeature(), self.nodes))

    def tests(self):
        return list(filter(lambda node: node.isTest(), self.nodes))

    def source_code(self):
        return list(filter(lambda node: node.isCode(), self.nodes))
