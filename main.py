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
    traceability_graph.export('/Users/ioanarotaru/Desktop/Disertatie/Model/TraceabilityGraphBuilder/out')


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
