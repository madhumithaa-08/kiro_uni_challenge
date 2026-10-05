def two_sum(nums, target):
    """Return indices of the two numbers adding up to target.

    Single hash-map pass: O(n) time, O(n) space.
    """
    seen = {}
    for i, n in enumerate(nums):
        if target - n in seen:
            return [seen[target - n], i]
        seen[n] = i
    return []
