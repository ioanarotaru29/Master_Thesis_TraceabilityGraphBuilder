from models.traceability_graph import TraceabilityGraph
from models.utils.gherkin_parser import GherkinParser

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    graph = TraceabilityGraph("/Users/ioanarotaru/Desktop/Disertatie/Data/P10_Data_springmvc-router/src")
    graph.build()
    print(graph.nodes)
