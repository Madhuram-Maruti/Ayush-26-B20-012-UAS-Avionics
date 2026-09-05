import heapq
import time
import os
import matplotlib
matplotlib.use("Agg")  # Write image files directly, no GUI window
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Path where this script file lives (Desktop)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


# ======================================================================
# STEP 1 - Reading the grid
# ======================================================================
def parse_grid(grid_lines):
    start, goal = None, None
    for r, row in enumerate(grid_lines):
        for c, ch in enumerate(row):
            if ch == 'S':
                start = (r, c)
            elif ch == 'G':
                goal = (r, c)
    if start is None or goal is None:
        raise ValueError("Grid must contain exactly one 'S' and one 'G'")
    return grid_lines, start, goal


def is_walkable(grid, row, col):
    if row < 0 or row >= len(grid):
        return False
    if col < 0 or col >= len(grid[0]):
        return False
    return grid[row][col] != '#'


# ======================================================================
# STEP 2 - The heuristic function h(n)
# ======================================================================
def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# ======================================================================
# STEP 3 - A* search
# ======================================================================
def a_star(grid, start, goal):
    t0 = time.perf_counter()

    g_score = {start: 0}
    came_from = {}
    open_set = [(manhattan_distance(start, goal), start)]

    explored = []
    expanded = set()

    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

    while open_set:
        _, current = heapq.heappop(open_set)

        if current in expanded:
            continue
        expanded.add(current)
        explored.append(current)

        if current == goal:
            path = [current]
            while path[-1] != start:
                path.append(came_from[path[-1]])
            path.reverse()
            return {
                "path": path,
                "cost": g_score[current],
                "explored": explored,
                "time": time.perf_counter() - t0,
            }

        for dr, dc in moves:
            neighbor = (current[0] + dr, current[1] + dc)
            if not is_walkable(grid, *neighbor):
                continue

            tentative_g = g_score[current] + 1

            if tentative_g < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + manhattan_distance(neighbor, goal)
                heapq.heappush(open_set, (f_score, neighbor))

    return {
        "path": None,
        "cost": None,
        "explored": explored,
        "time": time.perf_counter() - t0,
    }


# ======================================================================
# STEP 4 - Visualization
# ======================================================================
def visualize(grid, result, start, goal, title, save_path):
    n_rows, n_cols = len(grid), len(grid[0])
    fig, ax = plt.subplots(figsize=(n_cols * 0.55 + 1.5, n_rows * 0.55 + 1.5))

    for r in range(n_rows):
        for c in range(n_cols):
            color = "#3a3a3a" if grid[r][c] == "#" else "white"
            ax.add_patch(patches.Rectangle((c, r), 1, 1, facecolor=color, edgecolor="#cccccc"))

    for (r, c) in result["explored"]:
        if grid[r][c] != "#":
            ax.add_patch(patches.Rectangle((c, r), 1, 1, facecolor="#a8d4f0", edgecolor="#cccccc"))

    if result["path"]:
        xs = [c + 0.5 for (_, c) in result["path"]]
        ys = [r + 0.5 for (r, _) in result["path"]]
        ax.plot(xs, ys, color="crimson", linewidth=3, marker="o", markersize=4, zorder=5)

    ax.text(start[1] + 0.5, start[0] + 0.5, "S", ha="center", va="center",
            fontsize=13, fontweight="bold", color="darkgreen", zorder=6)
    ax.text(goal[1] + 0.5, goal[0] + 0.5, "G", ha="center", va="center",
            fontsize=13, fontweight="bold", color="darkred", zorder=6)

    ax.set_xlim(0, n_cols)
    ax.set_ylim(0, n_rows)
    ax.invert_yaxis()
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    found = "path found" if result["path"] else "NO PATH FOUND"
    ax.set_title(f"{title}\n({found}, {len(result['explored'])} nodes explored)", fontsize=10)
    plt.tight_layout()
    plt.savefig(save_path, dpi=130)
    plt.close(fig)


# ======================================================================
# STEP 5 - Test grids
# ======================================================================
TEST_CASES = [
    {
        "name": "Test Case 1: Simple Path",
        "grid": [
            "S.......",
            "..###...",
            "....#...",
            ".#..#...",
            ".#......",
            "........",
            "........",
            ".......G",
        ],
    },
    {
        "name": "Test Case 2: Multiple Possible Paths",
        "grid": [
            ".........",
            "....#....",
            "....#....",
            "....#....",
            "S...#...G",
            "....#....",
            "....#....",
            "....#....",
            ".........",
        ],
    },
    {
        "name": "Test Case 3: Narrow Passage",
        "grid": [
            "S..##...",
            "...##...",
            "...##...",
            "...##...",
            "...##...",
            "........",
            "...##...",
            "...##...",
            "...##...",
            "...##..G",
        ],
    },
    {
        "name": "Test Case 4: Different Obstacle Arrangement",
        "grid": [
            "S.....##..",
            "#....#...#",
            "#......#..",
            "##.#.####.",
            "..#...#.#.",
            "....##...#",
            ".####.....",
            ".##.#.##..",
            ".......#..",
            "#....##.#G",
        ],
    },
    {
        "name": "Test Case 5: No Valid Path",
        "grid": [
            "S.......",
            "........",
            "........",
            "########",
            "........",
            "........",
            "........",
            ".......G",
        ],
    },
]


# ======================================================================
# STEP 6 - Run tests
# ======================================================================
def run_all_tests():
    log_lines = []

    def log(msg=""):
        print(msg)
        log_lines.append(msg)

    for i, case in enumerate(TEST_CASES, start=1):
        grid, start, goal = parse_grid(case["grid"])
        result = a_star(grid, start, goal)

        log("-----------Search Result-----------")
        log(case["name"])
        if result["path"]:
            log("Path Found: YES")
            log("Path:")
            for p in result["path"]:
                log(f"  {p}")
            log(f"Total Path Cost: {result['cost']}")
        else:
            log("Path Found: NO")
            log("No valid path exists between Start and Goal.")
        log(f"Nodes Explored: {len(result['explored'])}")
        log(f"Execution Time: {result['time']:.6f} seconds")

        img_filename = f"testcase_{i}.png"
        full_img_path = os.path.join(SCRIPT_DIR, img_filename)
        visualize(grid, result, start, goal, case["name"], full_img_path)
        log(f"Visualization saved: {img_filename}")
        log("")

    log_file_path = os.path.join(SCRIPT_DIR, "simulation_log.txt")
    with open(log_file_path, "w") as f:
        f.write("\n".join(log_lines))


if __name__ == "__main__":
    run_all_tests()