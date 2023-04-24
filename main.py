import sys

from graph import Graph

if __name__ == '__main__':
    traceability_graph = Graph('/Users/ioanarotaru/Desktop/Disertatie/Data/P10_Data_trivial-graph') #sys.argv[1])
    print([node.fileName for node in traceability_graph.features()])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
