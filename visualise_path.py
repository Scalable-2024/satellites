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
    "A": {
        "B": [
            [
                "E",
                "D",
                "C",
                "B"
            ],
            [
                "C",
                "E",
                "D",
                "B"
            ]
        ],
        "C": [
            [
                "B",
                "D",
                "E",
                "C"
            ],
            [
                "D",
                "B",
                "E",
                "C"
            ]
        ],
        "D": [
            [
                "E",
                "B",
                "C",
                "D"
            ],
            [
                "C",
                "B",
                "E",
                "D"
            ]
        ],
        "E": [
            [
                "D",
                "B",
                "C",
                "E"
            ],
            [
                "B",
                "C",
                "D",
                "E"
            ]
        ]
    },
    "B": {
        "A": [
            [
                "E",
                "C",
                "D",
                "A"
            ],
            [
                "C",
                "E",
                "D",
                "A"
            ]
        ],
        "C": [
            [
                "D",
                "A",
                "E",
                "C"
            ],
            [
                "E",
                "A",
                "D",
                "C"
            ]
        ],
        "D": [
            [
                "A",
                "E",
                "C",
                "D"
            ],
            [
                "C",
                "E",
                "A",
                "D"
            ]
        ],
        "E": [
            [
                "D",
                "C",
                "A",
                "E"
            ],
            [
                "C",
                "D",
                "A",
                "E"
            ]
        ]
    },
    "C": {
        "A": [
            [
                "D",
                "E",
                "B",
                "A"
            ],
            [
                "D",
                "B",
                "E",
                "A"
            ]
        ],
        "B": [
            [
                "A",
                "E",
                "D",
                "B"
            ],
            [
                "E",
                "A",
                "D",
                "B"
            ]
        ],
        "D": [
            [
                "B",
                "E",
                "A",
                "D"
            ],
            [
                "E",
                "A",
                "B",
                "D"
            ]
        ],
        "E": [
            [
                "D",
                "B",
                "A",
                "E"
            ],
            [
                "D",
                "A",
                "B",
                "E"
            ]
        ]
    },
    "D": {
        "A": [
            [
                "B",
                "C",
                "E",
                "A"
            ],
            [
                "C",
                "E",
                "B",
                "A"
            ]
        ],
        "B": [
            [
                "C",
                "A",
                "E",
                "B"
            ],
            [
                "E",
                "A",
                "C",
                "B"
            ]
        ],
        "C": [
            [
                "A",
                "E",
                "B",
                "C"
            ],
            [
                "B",
                "A",
                "E",
                "C"
            ]
        ],
        "E": [
            [
                "A",
                "C",
                "B",
                "E"
            ],
            [
                "B",
                "A",
                "C",
                "E"
            ]
        ]
    },
    "E": {
        "A": [
            [
                "C",
                "B",
                "D",
                "A"
            ],
            [
                "B",
                "D",
                "C",
                "A"
            ]
        ],
        "B": [
            [
                "C",
                "A",
                "D",
                "B"
            ],
            [
                "D",
                "A",
                "C",
                "B"
            ]
        ],
        "C": [
            [
                "A",
                "B",
                "D",
                "C"
            ],
            [
                "B",
                "A",
                "D",
                "C"
            ]
        ],
        "D": [
            [
                "C",
                "A",
                "B",
                "D"
            ],
            [
                "A",
                "C",
                "B",
                "D"
            ]
        ]
    }
}
plot_network_graph(data)
