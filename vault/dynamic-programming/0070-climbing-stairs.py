def climb_stairs(n):
    """Number of distinct ways to climb n stairs taking 1 or 2 steps.

    Bottom-up DP with rolling variables: O(n) time, O(1) space.
    """
    if n <= 2:
        return n
    prev, cur = 1, 2
    for _ in range(3, n + 1):
        prev, cur = cur, prev + cur
    return cur
