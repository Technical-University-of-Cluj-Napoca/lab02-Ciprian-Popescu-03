from collections import deque
import sys

def read_maze(filename: str) -> list[list[str]]:
    """Reads a maze from a file into a 2D list (matrix)."""
    maze: list[list[str]] = []
    try:
        with open(filename, 'r') as file:
            maze = [list(line.rstrip()) for line in file.readlines()]
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    return maze


def find_start_and_target(maze: list[list[str]]) -> tuple[tuple[int,int], tuple[int,int]]:
    """Finds coordinates of start 'S' and target 'T'."""
    start = (-1, -1)
    target = (-1, -1)
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if cell == 'S':
                start = (i, j)
            elif cell == 'T':
                target = (i, j)
    return start, target


def get_neighbors(maze: list[list[str]], position: tuple[int,int]) -> list[tuple[int,int]]:
    """Returns valid neighbors (up, down, left, right) not blocked by walls."""
    directions = [(-1,0),(1,0),(0,-1),(0,1)]
    neighbors = []
    for dr, dc in directions:
        r, c = position[0]+dr, position[1]+dc
        if 0 <= r < len(maze) and 0 <= c < len(maze[0]) and maze[r][c] != '#':
            neighbors.append((r, c))
    return neighbors


def bfs(maze: list[list[str]], start: tuple[int,int], target: tuple[int,int]) -> list[tuple[int,int]]:
    """Breadth-First Search to find shortest path from start to target."""
    queue = deque()
    queue.append((start, [start]))
    visited = set()
    visited.add(start)

    while queue:
        current, path = queue.popleft()
        if current == target:
            return path
        for neighbor in get_neighbors(maze, current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    return []


def dfs(maze: list[list[str]], start: tuple[int,int], target: tuple[int,int]) -> list[tuple[int,int]]:
    """Depth-First Search to find a path from start to target."""
    stack = [(start, [start])]
    visited = set()
    visited.add(start)

    while stack:
        current, path = stack.pop()
        if current == target:
            return path
        for neighbor in get_neighbors(maze, current):
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append((neighbor, path + [neighbor]))
    return []


def print_maze_with_path(maze: list[list[str]], path: list[tuple[int,int]], start, target):
    """Print maze with path using ANSI colors:
       red '*' for path, yellow 'S' for start, green 'T' for target.
    """
    RED = "\033[91m"
    YELLOW = "\033[93m"
    GREEN = "\033[92m"
    RESET = "\033[0m"

    maze_copy = [row.copy() for row in maze]

    for r, c in path:
        if maze_copy[r][c] not in ('S', 'T'):
            maze_copy[r][c] = RED + '*' + RESET

    sr, sc = start
    tr, tc = target
    maze_copy[sr][sc] = YELLOW + 'S' + RESET
    maze_copy[tr][tc] = GREEN + 'T' + RESET

    for row in maze_copy:
        print(''.join(row))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python maze_search.py <bfs|dfs> <maze_filename>")
        sys.exit(1)

    algorithm = sys.argv[1].lower()
    filename = sys.argv[2]

    maze = read_maze(filename)
    if not maze:
        sys.exit(1)

    start, target = find_start_and_target(maze)
    if start == (-1, -1) or target == (-1, -1):
        print("Error: Start ('S') or Target ('T') not found in maze.")
        sys.exit(1)

    if algorithm == "bfs":
        path = bfs(maze, start, target)
    elif algorithm == "dfs":
        path = dfs(maze, start, target)
    else:
        print("Error: Unknown algorithm. Use 'bfs' or 'dfs'.")
        sys.exit(1)

    if path:
        print("\nPath found:")
        print(path)
        print("\nMaze with solution path:")
        print_maze_with_path(maze, path, start, target)
    else:
        print("No path found from start to target.")
