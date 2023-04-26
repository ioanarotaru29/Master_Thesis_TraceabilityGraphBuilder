import sys

from models.traceability_graph import TraceabilityGraph

if __name__ == '__main__':
    traceability_graph = TraceabilityGraph(
        # '/Users/ioanarotaru/Desktop/Disertatie/Data/P10_Data_springmvc-router')
        '/Users/ioanarotaru/Desktop/Disertatie/Data/P10_Data_trivial-graph')
        # #sys.argv[1])
    traceability_graph.build()
    # print([node.fileName for node in traceability_graph.features()])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
