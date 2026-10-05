def is_valid(s):
    """Return True if the bracket string is balanced and correctly nested.

    Single pass with a stack: O(n) time, O(n) space.
    """
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in s:
        if ch in "([{":
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
    return not stack
