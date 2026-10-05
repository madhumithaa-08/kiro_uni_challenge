def num_islands(grid):
    """Count connected components of '1' cells using iterative DFS.

    O(rows * cols) time; O(rows * cols) space in the worst case (stack).
    """
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])
    count = 0

    def sink(r, c):
        stack = [(r, c)]
        while stack:
            x, y = stack.pop()
            if 0 <= x < rows and 0 <= y < cols and grid[x][y] == "1":
                grid[x][y] = "0"
                stack.extend([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                count += 1
                sink(r, c)
    return count
