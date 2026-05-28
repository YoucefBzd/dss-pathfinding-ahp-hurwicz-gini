import heapq
import itertools
from data import CITIES, build_graph, euclidean
from gini import gini


def min_cost_per_unit(graph):
    """Smallest Expected-Cost-per-distance ratio over all edges.
    Multiplying the straight-line distance by this keeps h admissible."""
    ratios = []
    for a in graph:
        for b, ec in graph[a]:
            d = euclidean(a, b)
            if d > 0:
                ratios.append(ec / d)
    return min(ratios)


def heuristic(city, goal, k):
    """Admissible heuristic: straight-line distance * cheapest cost per unit."""
    return euclidean(city, goal) * k


def astar(graph, start, goal, lam=0.0):
    """
    Run the hybrid A* search.
    lam : the Gini penalty weight (lambda). lam=0 gives the classic A*.
    Returns a dict (path, base_cost, gini, equitable_cost) or None.
    """
    k = min_cost_per_unit(graph)
    counter = itertools.count()        # unique tie-breaker for the heap

    # Heap item: (f, count, current_city, path_so_far, edge_costs_so_far)
    frontier = [(heuristic(start, goal, k), next(counter), start, [start], [])]

    while frontier:
        f, _, city, path, edge_costs = heapq.heappop(frontier)

        if city == goal:                       # goal reached
            base = sum(edge_costs)
            g_val = gini(edge_costs)
            return {
                "path": path,
                "base_cost": base,
                "gini": g_val,
                "equitable_cost": base + lam * g_val,
            }

        for neighbor, ec in graph[city]:       # expand neighbours
            if neighbor in path:               # never visit the same city twice
                continue
            new_path = path + [neighbor]
            new_costs = edge_costs + [ec]
            g_eq = sum(new_costs) + lam * gini(new_costs)
            new_f = g_eq + heuristic(neighbor, goal, k)
            heapq.heappush(frontier,
                           (new_f, next(counter), neighbor, new_path, new_costs))

    return None


# --- Self-test: Alger -> Constantine, without and with the Gini penalty ---
if __name__ == "__main__":
    from ahp import compute_weights
    from data import AHP_MATRIX

    weights = compute_weights(AHP_MATRIX)
    graph = build_graph(weights, alpha=0.6)
    start, goal = "Alger", "Constantine"

    print(f"=== Hybrid A* search: {start} -> {goal} ===\n")

    for lam in (0, 80):
        res = astar(graph, start, goal, lam=lam)
        tag = "classic A* (lambda=0)" if lam == 0 else f"equitable A* (lambda={lam})"
        print(f"[{tag}]")
        print("  Path          :", " -> ".join(res["path"]))
        print(f"  Base cost     : {res['base_cost']:.2f}")
        print(f"  Gini (equity) : {res['gini']:.3f}")
        print(f"  Equitable cost: {res['equitable_cost']:.2f}\n")