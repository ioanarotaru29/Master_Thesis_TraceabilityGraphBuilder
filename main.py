import sys

import numpy as np
from gensim.models import Word2Vec
from matplotlib import pyplot as plt
from sklearn.manifold import TSNE

from models.traceability_graph import TraceabilityGraph

if __name__ == '__main__':
    traceability_graph = TraceabilityGraph(
        # '/Users/ioanarotaru/Desktop/Disertatie/Data/P10_Data_springmvc-router')
        '/Users/ioanarotaru/Desktop/Disertatie/Data/P10_Data_trivial-graph')
        # #sys.argv[1])
    traceability_graph.build()

    all_keywords = []
    sentences = []
    for nodes in traceability_graph.nodes.values():
        for node in nodes:
            all_keywords += node.keywords()
            sentences.append(node.keywords())
    all_keywords = set(all_keywords)

    model = Word2Vec(window=5, min_count=1)
    model.build_vocab(corpus_iterable=sentences)
    model.train(corpus_iterable=sentences, total_examples=len(sentences), epochs=50)

    feature = traceability_graph.nodes.get('FEATURE')[0]
    target_sentence_words = feature.keywords()
    result = []
    for node in traceability_graph.nodes.get('TEST'):
        sentence = node.keywords()
        sim = model.wv.n_similarity(target_sentence_words, sentence)
        result.append([feature.name(), node.name(), sim])
    result.sort(key=lambda x: x[2])
    print(result)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
