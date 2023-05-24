import fnmatch
import os
import re

from models.utils.gherkin_parser import GherkinParser
from models.utils.java_class_parser import JavaClassParser


class TraceabilityGraph:
    FILES_TO_INCLUDE = ['*.feature', '*.java']

    def __init__(self, location):
        self.__location = location
        self.nodes = {
            'REQUIREMENTS': [],
            'TEST_CASES': [],
            'SOURCE_CODE': []
        }
        self.edges = {}

    def build(self):
        for path, subdirs, files in os.walk(self.__location):
            for file in files:
                # Allow only Java source files or Gherkin files
                includes = r'|'.join([fnmatch.translate(x) for x in self.FILES_TO_INCLUDE])
                file_path = os.path.join(path, file)
                if re.match(includes, file_path):
                    if re.search(r'\.feature$', file_path):
                        self.__parseFeatureFile(file_path)
                    elif re.search(r'/src/main/', file_path):
                        self.__parseSourceCodeFile(file_path)

    def __parseFeatureFile(self, file_path):
        parser = GherkinParser(file_path)
        req, tests = parser.parse()

        if req is not None:
            self.nodes['REQUIREMENTS'].append(req)
        self.nodes['TEST_CASES'] += tests

    def __parseSourceCodeFile(self, file_path):
        parser = JavaClassParser(file_path)
        source_code = parser.parse()
        if source_code is not None:
            self.nodes['SOURCE_CODE'].append(source_code)
