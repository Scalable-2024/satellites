import networkx as nx
import matplotlib.pyplot as plt


def plot_network_graph(data):
    """
    Plots a network graph based on the given JSON-like dictionary.
    
    :param data: Dictionary where keys are nodes and values are dictionaries of connected nodes and paths.
    """
    # Create a directed graph
    G = nx.DiGraph()

    # Add nodes and edges with path labels
    for source, connections in data.items():
        for target, paths in connections.items():
            for path in paths:
                # Adding edge with path as label
                G.add_edge(source, target, label=str(path))

    # Set up graph layout
    pos = nx.spring_layout(G)  # Positions for all nodes

    # Draw nodes and edges
    nx.draw(G, pos, with_labels=True, node_size=700, node_color='lightblue',
            font_size=10, font_weight='bold', arrowsize=15)

    # Draw edge labels
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(
        G, pos, edge_labels=edge_labels, font_size=8, font_color='red')

    # Show plot
    plt.title("Network Graph")
    plt.show()
    # plt.savefig('output.png')



# Example usage
data = {"A": {"B": [["E", "B"]], "C": [["C"]], "D": [["D"]], "E": [["E"]]}, "B": {"A": [["A"]], "C": [["D", "C"]], "D": [["D"]], "E": [["E"]]}, "C": {"A": [["A"]], "B": [["B"]], "D": [["D"]], "E": [["E"]]}, "D": {"A": [["A"]], "B": [["B"]], "C": [["A", "C"]], "E": [["E"]]}, "E": {"A": [["A"]], "B": [["C", "B"]], "C": [["A", "C"]], "D": [["D"]]}}
plot_network_graph(data)
