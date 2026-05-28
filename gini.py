import numpy as np


def gini(costs):
    """Compute the Gini coefficient of a list of edge costs (0 = balanced)."""
    x = np.array(costs, dtype=float)
    n = len(x)
    if n <= 1:                # a path with 0 or 1 edge cannot be unequal
        return 0.0
    mean = x.mean()
    if mean == 0:             # avoid division by zero if all costs are 0
        return 0.0
    total_diff = np.sum(np.abs(x[:, None] - x[None, :]))   # sum over all pairs
    return total_diff / (2 * n**2 * mean)


# --- Self-test: show the intuition with three example routes ---
if __name__ == "__main__":
    print("=== Gini self-test (equity intuition) ===\n")
    examples = {
        "Perfectly balanced [10, 10, 10, 10]": [10, 10, 10, 10],
        "Slightly unbalanced [10, 12, 9, 11]": [10, 12, 9, 11],
        "One dangerous leg   [5, 5, 5, 100]":  [5, 5, 5, 100],
    }
    for label, costs in examples.items():
        g = gini(costs)
        print(f"  {label}  ->  Gini = {g:.3f}")
    print("\n  Reading: closer to 0 = fair/balanced route,")
    print("           closer to 1 = one leg carries most of the risk.")