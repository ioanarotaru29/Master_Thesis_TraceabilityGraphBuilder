import fnmatch
import os
import re

from gensim.models import Word2Vec

from models.edge import Edge
from models.node import Node
from models.utils.text_sanitizer import TextSanitizer


class TraceabilityGraph:
    FILES_TO_INCLUDE = ['*.feature', '*.java']

    def __init__(self, location, window=5, min_count=1, epochs=50, treshold=0.75):
        self.__location = location
        self.__sanitizer = TextSanitizer()
        self.__model = Word2Vec(window=window, min_count=min_count)
        self.__epochs = epochs
        self.__treshold = treshold

        self.nodes = {}
        self.edges = []

    def __build_node(self, file_path):
        # Allow only Java source files or Gherkin files
        includes = r'|'.join([fnmatch.translate(x) for x in self.FILES_TO_INCLUDE])
        if not re.match(includes, file_path):
            return None

        if re.search(r'\.feature$', file_path):
            return Node(file_path, 'FEATURE', sanitizer=self.__sanitizer)
        elif re.search(r'/src/test/', file_path):
            return Node(file_path, 'TEST', sanitizer=self.__sanitizer)
        elif re.search(r'/src/main/', file_path):
            return Node(file_path, 'CODE', sanitizer=self.__sanitizer)
        else:
            return None

    def __build_nodes(self):
        for path, subdirs, files in os.walk(self.__location):
            for file in files:
                node = self.__build_node(os.path.join(path, file))
                if node is not None:
                    if node.type() not in self.nodes.keys():
                        self.nodes[node.type()] = []
                    self.nodes[node.type()].append(node)

    def __build_dependencies(self, source_type, target_type):
        print("FROM:", source_type, " TO:", target_type)
        for source_node in self.nodes.get(source_type):
            for target_node in self.nodes.get(target_type):
                sim = self.__model.wv.n_similarity(source_node.keywords(), target_node.keywords())
                edge = Edge(source_node, target_node, sim)

                if sim >= self.__treshold:
                    self.edges.append(edge)
                print(source_node.name(), target_node.name(), sim)

    def build(self):
        print("Building nodes...")
        self.__build_nodes()

        sentences = []
        for type_nodes in self.nodes.values():
            sentences += list(map(lambda x: x.keywords(), type_nodes))
        self.__model.build_vocab(corpus_iterable=sentences)
        self.__model.train(corpus_iterable=sentences, total_examples=len(sentences), epochs=self.__epochs)

        print("Building dependencies...")
        self.__build_dependencies('FEATURE', 'TEST')
        self.__build_dependencies('TEST', 'CODE')

    def export_nodes(self, path, node_type):
        with open(os.path.join(path, node_type.lower() + 's.csv'), 'w') as f:
            f.write('id, name, location\n')

            nodes = self.nodes.get(node_type)
            for idx, nodes in enumerate(nodes):
                fields = [str(idx + 1), nodes.name(), nodes.location()]
                f.write(', '.join(fields) + '\n')

    def export_dependencies(self, path, source_type, target_type):
        with open(os.path.join(path, source_type.lower() + '_to_' + target_type.lower() + '.csv'), 'w') as f:
            f.write('source_id, target_id, cosine_similarity\n')

            edges = list(filter(lambda x: x.source.type() == source_type and x.target.type() == target_type,
                                self.edges))
            for edge in edges:
                source_idx = self.nodes.get(edge.source.type()).index(edge.source)
                target_idx = self.nodes.get(edge.target.type()).index(edge.target)
                sim = edge.similarity
                f.write(', '.join([str(source_idx + 1), str(target_idx + 1), str(sim)]) + '\n')

    def export(self, path):
        for node_type in ['FEATURE', 'TEST', 'CODE']:
            self.export_nodes(path, node_type)
        self.export_dependencies(path, 'FEATURE', 'TEST')
        self.export_dependencies(path, 'TEST', 'CODE')
