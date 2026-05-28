def expected_cost(min_cost, max_cost, alpha):
    """
    Compute the Hurwicz expected cost of ONE edge.

    min_cost : best-case (lowest) cost of the edge
    max_cost : worst-case (highest) cost of the edge
    alpha    : optimism factor between 0 and 1
    """
    return alpha * min_cost + (1 - alpha) * max_cost


# --- Self-test: reproduce the grocer example from Chapter 1 (slide 70) ---
# The grocer example uses PROFITS (we maximize), so "best" = max profit.
if __name__ == "__main__":
    alpha = 0.7
    grocer = [
        ("Small Order",  50, 50),    # (name, worst_profit, best_profit)
        ("Medium Order", 42, 52),
        ("Large Order",  34, 54),
    ]

    print("=== Hurwicz self-test (Chapter 1 grocer example, alpha=0.7) ===")
    print("Profit version: WA = alpha*Best + (1-alpha)*Worst\n")
    best_choice, best_value = None, -1
    for name, worst, best in grocer:
        wa = alpha * best + (1 - alpha) * worst
        print(f"  {name:<13}: ({alpha}*{best}) + ({1-alpha:.1f}*{worst}) = {wa:.0f}")
        if wa > best_value:
            best_value, best_choice = wa, name
    print(f"\n  Best alternative: {best_choice} (highest weighted average)")

    print("\n=== Cost version used in the project ===")
    print("EC = alpha*Min_Cost + (1-alpha)*Max_Cost")
    ec = expected_cost(min_cost=10, max_cost=30, alpha=0.7)
    print(f"  Edge with min=10, max=30, alpha=0.7  ->  EC = {ec:.1f}")