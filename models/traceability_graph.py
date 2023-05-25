import fnmatch
import os
import re

from gensim.models import Word2Vec

from models.edge import Edge
from models.utils.gherkin_parser import GherkinParser
from models.utils.java_class_parser import JavaClassParser
from models.utils.java_test_parser import JavaTestParser
from models.utils.text_sanitizer import TextSanitizer
from models.utils.xml_results_parser import XmlResultsParser


class TraceabilityGraph:
    FILES_TO_INCLUDE = ['*.feature', '*.java']

    def __init__(self, location, test_results_location=None, mutations_location=None, 
                 window=5, min_count=1, epochs=25):
        self.__location = location
        self.__test_results_location = test_results_location
        self.__mutations_location = mutations_location
        
        self.__sanitizer = TextSanitizer()
        self.__model = Word2Vec(window=window, min_count=min_count)
        self.__epochs = epochs

        self.nodes = {
            'REQUIREMENTS': [],
            'TEST_CASES': [],
            'SOURCE_CODE': []
        }
        self.edges = {
            'REQUIREMENTS_TO_TEST_CASES': [],
            'TEST_CASES_TO_SOURCE_CODE': [],
            'TEST_CASES_TO_FAULTS': []
        }

    def build(self):
        print("Parse project files...")
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
                    elif re.search(r'/src/test/', file_path):
                        self.__parseTestCodeFile(file_path)

        if self.__test_results_location is not None:
            self.__parseTestResults()
        
        print("Sanitize project files...")
        for _, nodes in self.nodes.items():
            for node in nodes:
                self.__sanitize_node(node)

        print("Detect dependencies...")
        sentences = []
        for type_nodes in self.nodes.values():
            sentences += list(map(lambda x: x.sentences, type_nodes))
        self.__model.build_vocab(corpus_iterable=sentences)
        self.__model.train(corpus_iterable=sentences, total_examples=len(sentences), epochs=self.__epochs)

        self.__build_dependencies('REQUIREMENTS', 'TEST_CASES')
        self.__build_dependencies('TEST_CASES', 'SOURCE_CODE')


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

    def __parseTestCodeFile(self, file_path):
        parser = JavaTestParser(file_path)
        test_case, general_sentences, annotated_sentences = parser.parse()
        if len(annotated_sentences.keys()) > 0:
            for test in self.nodes['TEST_CASES']:
                keywords_to_add = []
                for sentence, keywords in annotated_sentences.items():
                    sentence = sentence.replace('"^', '^').replace('$"', '$')
                    if len(list(filter(lambda s: re.match(sentence, s), test.sentences))) > 0:
                        keywords_to_add += keywords
                if len(keywords_to_add) > 0:
                    test.code_sentences += keywords_to_add
                    test.code_sentences += general_sentences
        elif test_case.name.endswith('Test'):
            self.nodes['TEST_CASES'].append(test_case)

    def __sanitize_node(self, node):
        sentence = ' '.join(node.sentences)
        code_sentence = ' '.join(node.code_sentences)
        result = self.__sanitizer.sanitize(sentence, use_transform=False, use_entity_recognition=True) or []
        code_result = self.__sanitizer.sanitize(code_sentence, use_transform=True, use_entity_recognition=False) or []
        final_result = result + code_result
        if len(final_result) > 0:
            node.sentences = final_result

    def __build_dependencies(self, source_type, target_type):
        print("FROM:", source_type, " TO:", target_type)
        for source_node in self.nodes.get(source_type):
            for target_node in self.nodes.get(target_type):
                sim = self.__model.wv.n_similarity(source_node.sentences, target_node.sentences)
                edge = Edge(source_node, target_node, sim)

                self.edges[source_type + "_TO_" + target_type].append(edge)
                print(source_node.name, target_node.name, sim)

    def __parseTestResults(self):
        parser = XmlResultsParser(self.__test_results_location)
        durations, faults = parser.parse()
        for name, duration in durations.items():
            node = next(filter(lambda x: x.name == name, self.nodes['TEST_CASES']), None)
            if node is not None:
                node.duration = duration
