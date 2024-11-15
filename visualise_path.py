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


# Example usage
data = {
    "A": {"B": [["D", "B"]], "C": [["B", "C"]], "D": [["D"]], "E": [["E"]]},
    "B": {"A": [["A"]], "C": [["C"]], "D": [["E", "D"]], "E": [["A", "E"]]},
    "C": {"A": [["A"]], "B": [["B"]], "D": [["D"]], "E": [["E"]]},
    "D": {"A": [["A"]], "B": [["C", "B"]], "C": [["C"]], "E": [["C", "E"]]},
    "E": {"A": [["A"]], "B": [["B"]], "C": [["C"]], "D": [["B", "D"]]}
}

plot_network_graph(data)
