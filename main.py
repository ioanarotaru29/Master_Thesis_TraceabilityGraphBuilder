from models.traceability_graph import TraceabilityGraph
from models.utils.gherkin_parser import GherkinParser
from models.utils.java_test_parser import JavaTestParser
from models.utils.xml_results_parser import XmlResultsParser

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    graph = TraceabilityGraph("/Users/ioanarotaru/Desktop/Disertatie/Data/P10_Data_trivial-graph/neo4j",
                              test_results_location="/Users/ioanarotaru/Desktop/Disertatie/Data/P10_Data_trivial-graph/Test Results - All_Features_in__features.xml")
    graph.build()
    print(graph.nodes)

    # parser = XmlResultsParser("/Users/ioanarotaru/Desktop/Disertatie/Data/P10_Data_trivial-graph/Test Results - All_Features_in__features.xml")
    # parser.parse()