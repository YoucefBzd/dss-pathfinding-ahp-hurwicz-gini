import math
from ahp import compute_weights, consistency_ratio
from hurwicz import expected_cost

# 1. The map: each city has (x, y) coordinates (used by the A* heuristic)
CITIES = {
    "Oran":        (0, 8),
    "Alger":       (5, 9),
    "Constantine": (11, 9),
    "Setif":       (9, 7),
    "Biskra":      (9, 3),
    "Ghardaia":    (5, 1),
    "Ouargla":     (9, 0),
}

# 2. The four decision criteria and their AHP comparison matrix
# Order: Travel Time, Financial Cost, Security Risk, Environmental Impact
CRITERIA = ["Travel Time", "Financial Cost", "Security Risk", "Environmental Impact"]

AHP_MATRIX = [
    [1,    3,    1/2,  4  ],   # Travel Time
    [1/3,  1,    1/4,  2  ],   # Financial Cost
    [2,    4,    1,    5  ],   # Security Risk
    [1/4,  1/2,  1/5,  1  ],   # Environmental Impact
]

# 3. Uncertainty band per criterion: (best_factor, worst_factor)
# Security is the most volatile; cost is the most stable.
UNCERTAINTY = {
    "Travel Time":          (0.8, 1.3),
    "Financial Cost":       (0.9, 1.1),
    "Security Risk":        (0.6, 1.8),
    "Environmental Impact": (0.85, 1.2),
}

# 4. The roads: nominal cost per criterion
#    [Travel Time, Financial Cost, Security Risk, Environmental Impact]
EDGES = {
    ("Oran", "Alger"):         [40, 30, 3, 6],
    ("Alger", "Setif"):        [35, 25, 4, 5],
    ("Alger", "Constantine"):  [55, 45, 5, 8],
    ("Alger", "Ghardaia"):     [60, 40, 6, 7],
    ("Setif", "Constantine"):  [20, 15, 2, 3],
    ("Setif", "Biskra"):       [30, 22, 5, 4],
    ("Constantine", "Biskra"): [40, 35, 7, 6],
    ("Biskra", "Ouargla"):     [50, 38, 8, 9],
    ("Biskra", "Ghardaia"):    [45, 30, 4, 5],
    ("Ghardaia", "Ouargla"):   [25, 20, 3, 4],
}


def euclidean(city_a, city_b):
    """Straight-line distance between two cities (for the heuristic)."""
    xa, ya = CITIES[city_a]
    xb, yb = CITIES[city_b]
    return math.hypot(xa - xb, ya - yb)


def build_graph(weights, alpha):
    """
    Build the final weighted graph.
    For each edge:
      - generalized BEST cost  = sum(weight_k * nominal_k * best_factor_k)
      - generalized WORST cost = sum(weight_k * nominal_k * worst_factor_k)
      - Expected Cost (EC)     = Hurwicz blend of best and worst
    Returns: graph dict  city -> list of (neighbor, EC) tuples (undirected)
    """
    graph = {city: [] for city in CITIES}
    for (a, b), nominal in EDGES.items():
        best = worst = 0.0
        for k, crit in enumerate(CRITERIA):
            bf, wf = UNCERTAINTY[crit]
            best  += weights[k] * nominal[k] * bf
            worst += weights[k] * nominal[k] * wf
        ec = expected_cost(min_cost=best, max_cost=worst, alpha=alpha)
        graph[a].append((b, ec))
        graph[b].append((a, ec))   # undirected road
    return graph


# --- Self-test: compute AHP weights and show each edge's Expected Cost ---
if __name__ == "__main__":
    weights = compute_weights(AHP_MATRIX)
    cr = consistency_ratio(AHP_MATRIX, weights)

    print("=== Criteria weights (AHP) ===")
    for name, w in zip(CRITERIA, weights):
        print(f"  {name:<22}: {w*100:5.1f}%")
    print(f"  Consistency Ratio (CR): {cr:.4f}  "
          f"({'consistent' if cr <= 0.10 else 'REVISE'})\n")

    alpha = 0.6
    graph = build_graph(weights, alpha)
    print(f"=== Edge Expected Costs (Hurwicz, alpha={alpha}) ===")
    seen = set()
    for a in graph:
        for b, ec in graph[a]:
            if (b, a) not in seen:
                print(f"  {a:<12} -- {b:<12}: EC = {ec:5.2f}")
                seen.add((a, b))