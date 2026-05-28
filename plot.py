import matplotlib
matplotlib.use("Agg")          # save a PNG without needing a display window
import matplotlib.pyplot as plt
import networkx as nx

from data import CITIES, build_graph


def draw_route(graph, path, title, filename):
    """Draw the whole graph and highlight the given route in red."""
    G = nx.Graph()
    for city, (x, y) in CITIES.items():
        G.add_node(city, pos=(x, y))
    for a in graph:
        for b, ec in graph[a]:
            if not G.has_edge(a, b):
                G.add_edge(a, b, weight=round(ec, 1))

    pos = nx.get_node_attributes(G, "pos")
    route_edges = list(zip(path[:-1], path[1:]))

    plt.figure(figsize=(9, 6))
    nx.draw_networkx_nodes(G, pos, node_color="#cfe8ff",
                           node_size=1500, edgecolors="#1f6fb2")
    nx.draw_networkx_labels(G, pos, font_size=9, font_weight="bold")
    nx.draw_networkx_edges(G, pos, edge_color="#bbbbbb", width=1.5)
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7)
    nx.draw_networkx_edges(G, pos, edgelist=route_edges,
                           edge_color="#d62728", width=3.5)

    plt.title(title, fontsize=12, fontweight="bold")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()
    print(f"  Figure saved: {filename}")


# --- Self-test: draw the classic and the equitable routes ---
if __name__ == "__main__":
    from ahp import compute_weights
    from data import AHP_MATRIX
    from astar import astar

    weights = compute_weights(AHP_MATRIX)
    graph = build_graph(weights, alpha=0.6)
    classic = astar(graph, "Alger", "Constantine", lam=0)
    equitable = astar(graph, "Alger", "Constantine", lam=80)

    print("Generating figures...")
    draw_route(graph, classic["path"],
               "Classic A* (lambda=0)  -  Gini = %.3f" % classic["gini"],
               "route_classic.png")
    draw_route(graph, equitable["path"],
               "Equitable A* (lambda=80)  -  Gini = %.3f" % equitable["gini"],
               "route_equitable.png")
    print("Done.")