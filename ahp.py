import numpy as np

# Random Index (RI) table from the course (Saaty).
RANDOM_INDEX = {1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90,
                5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41}


def compute_weights(matrix):
    """
    Step 2 of AHP: normalize the matrix and compute each criterion's weight.
    """
    matrix = np.array(matrix, dtype=float)
    column_sums = matrix.sum(axis=0)          # sum of each column
    normalized = matrix / column_sums         # normalize by column
    weights = normalized.mean(axis=1)         # weight = average of each row
    return weights


def consistency_ratio(matrix, weights):
    """
    Steps 3 to 6 of AHP: check the judgments' consistency.
    Returns CR. If CR <= 0.10 the judgments are acceptable.
    """
    matrix = np.array(matrix, dtype=float)
    n = matrix.shape[0]
    weighted_sum = matrix.dot(weights)             # Step 3
    lambda_max = (weighted_sum / weights).mean()   # Step 4
    ci = (lambda_max - n) / (n - 1)                # Step 5: Consistency Index
    ri = RANDOM_INDEX[n]
    cr = ci / ri if ri != 0 else 0.0               # Step 6: Consistency Ratio
    return cr


# --- Quick self-test: reproduce the Chapter 3 example ---
if __name__ == "__main__":
    course_matrix = [
        [1,     3,   2],     # Cost
        [1/3,   1,   1/2],   # Quality
        [1/2,   2,   1],     # Delivery Time
    ]
    criteria = ["Cost", "Quality", "Delivery Time"]

    w = compute_weights(course_matrix)
    cr = consistency_ratio(course_matrix, w)

    print("=== AHP self-test (Chapter 3 example) ===")
    for name, weight in zip(criteria, w):
        print(f"  {name:<15}: {weight*100:.1f}%")
    print(f"  Consistency Ratio (CR): {cr:.4f}")
    print("  Judgments are consistent." if cr <= 0.10
          else "  Judgments must be revised.")