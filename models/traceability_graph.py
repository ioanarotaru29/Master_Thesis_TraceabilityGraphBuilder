import fnmatch
import os
import re

from models.node import Node


class TraceabilityGraph:
    FILES_TO_INCLUDE = ['*.feature', '*.java']

    def __init__(self, location):
        self.__location = location
        self.nodes = []
        self.edges = []

    def __build_node(self, file_path):
        # Allow only Java source files or Gherkin files
        includes = r'|'.join([fnmatch.translate(x) for x in self.FILES_TO_INCLUDE])
        if not re.match(includes, file_path):
            return None

        if re.search(r'\.feature$', file_path):
            return Node(file_path, 'FEATURE')
        elif re.search(r'/src/test/', file_path):
            return Node(file_path, 'TEST')
        elif re.search(r'/src/main/', file_path):
            return Node(file_path, 'CODE')
        else:
            return None

    def build(self):
        for path, subdirs, files in os.walk(self.__location):
            for file in files:
                node = self.__build_node(os.path.join(path, file))
                if node is not None:
                    self.nodes.append(node)
