from ahp import compute_weights, consistency_ratio
from data import AHP_MATRIX, CRITERIA, build_graph
from astar import astar

# --- Experiment settings (change these to test other scenarios) ---
START = "Alger"
GOAL = "Constantine"
ALPHA = 0.6        # Hurwicz optimism factor (0 = pessimistic, 1 = optimistic)
LAMBDA = 80        # Gini penalty weight (0 = classic A*, higher = fairer)


def main():
    # 1. AHP: criteria weights + consistency check
    weights = compute_weights(AHP_MATRIX)
    cr = consistency_ratio(AHP_MATRIX, weights)

    print("=" * 58)
    print(" MULTI-CRITERIA PATHFINDING UNDER UNCERTAINTY (A* + Gini)")
    print("=" * 58)

    print("\n[1] AHP - Criteria weights")
    for name, w in zip(CRITERIA, weights):
        print(f"    {name:<22}: {w*100:5.1f}%")
    print(f"    Consistency Ratio (CR): {cr:.4f} "
          f"({'consistent' if cr <= 0.10 else 'REVISE'})")

    # 2. Hurwicz: build the weighted graph
    graph = build_graph(weights, alpha=ALPHA)
    print(f"\n[2] Hurwicz - Edge expected costs built (alpha = {ALPHA})")

    # 3. A* search: classic vs equitable
    print(f"\n[3] A* search: {START} -> {GOAL}\n")
    classic = astar(graph, START, GOAL, lam=0)
    equitable = astar(graph, START, GOAL, lam=LAMBDA)

    print(f"    Classic A* (lambda = 0):")
    print(f"      Route          : {' -> '.join(classic['path'])}")
    print(f"      Base cost      : {classic['base_cost']:.2f}")
    print(f"      Gini (equity)  : {classic['gini']:.3f}")

    print(f"\n    Equitable A* (lambda = {LAMBDA}):")
    print(f"      Route          : {' -> '.join(equitable['path'])}")
    print(f"      Base cost      : {equitable['base_cost']:.2f}")
    print(f"      Gini (equity)  : {equitable['gini']:.3f}")

    # 4. Conclusion
    print("\n[4] Conclusion")
    if classic["path"] != equitable["path"]:
        extra = equitable["base_cost"] - classic["base_cost"]
        drop = classic["gini"] - equitable["gini"]
        print(f"    The equitable route lowers the Gini by {drop:.3f}")
        print(f"    for only +{extra:.2f} in base cost: a fairer, safer trip.")
    else:
        print("    Both routes are identical: the cheapest route is also the")
        print("    most balanced one, so no trade-off is needed here.")
    print("=" * 58)
    return graph, classic, equitable


if __name__ == "__main__":
    main()