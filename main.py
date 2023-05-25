from models.traceability_graph import TraceabilityGraph
from models.utils.parsers.xml_mutations_parser import XmlMutationsParser

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # P10_Data_trivial-graph
    # graph = TraceabilityGraph("/Users/ioanarotaru/Desktop/Disertatie/Data/P10_Data_trivial-graph/neo4j",
    #                           test_results_location="/Users/ioanarotaru/Desktop/Disertatie/Data/P10_Data_trivial-graph/Test Results - All_Features_in__features.xml")
    # graph.build()
    # graph.export("/Users/ioanarotaru/Desktop/Disertatie/Model/TraceabilityGraphBuilder_Version2/out/P10_Data_trivial-graph")

    # P10_Data_P10_Data_springmvc-router
    graph = TraceabilityGraph("/Users/ioanarotaru/Desktop/Disertatie/Data/P10_Data_springmvc-router/src",
                              test_results_location="/Users/ioanarotaru/Desktop/Disertatie/Data/P10_Data_springmvc-router/Test Results - RunCucumberTest.xml",
                              mutations_location="/Users/ioanarotaru/Desktop/Disertatie/Data/P10_Data_springmvc-router/target/pit-reports/202305232104/mutations.xml")
    graph.build()
    graph.export("/Users/ioanarotaru/Desktop/Disertatie/Model/TraceabilityGraphBuilder_Version2/out/P10_Data_springmvc-router")