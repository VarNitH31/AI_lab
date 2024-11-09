import heapq

GOAL_STATE = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

def misplaced_tiles_heuristic(state, goal_state):
    misplaced_tiles = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != goal_state[i][j] and state[i][j] != 0:
                misplaced_tiles += 1
    return misplaced_tiles

class PuzzleNode:
    def __init__(self, state, parent=None, g=0, h=0):
        self.state = state
        self.parent = parent
        self.g = g  # Cost from start to current node
        self.h = h  # Heuristic cost to goal (misplaced tiles)
        self.f = g + h  # Total cost

    def __lt__(self, other):
        return self.f < other.f

def get_empty_tile(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

def generate_neighbors(node):
    neighbors = []
    x, y = get_empty_tile(node.state)

    moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    for dx, dy in moves:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < 3 and 0 <= new_y < 3:
            new_state = [row[:] for row in node.state]
            new_state[x][y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[x][y]
            h = misplaced_tiles_heuristic(new_state, GOAL_STATE)
            neighbors.append(PuzzleNode(new_state, node, node.g + 1, h))

    return neighbors

def is_goal_reached(state, goal_state):
    return state == goal_state

def reconstruct_path(node):
    path = []
    while node:
        path.append(node.state)
        node = node.parent
    return path[::-1]

def a_star_search(start_state):
    open_set = [PuzzleNode(start_state, h=misplaced_tiles_heuristic(start_state, GOAL_STATE))]
    closed_set = set()

    while open_set:
        current_node = heapq.heappop(open_set)

        if is_goal_reached(current_node.state, GOAL_STATE):
            return reconstruct_path(current_node)

        closed_set.add(tuple(map(tuple, current_node.state)))

        for neighbor in generate_neighbors(current_node):
            if tuple(map(tuple, neighbor.state)) not in closed_set:
                heapq.heappush(open_set, neighbor)

    return None

def get_user_input():
    while True:
        print("Enter your 8-puzzle configuration (0 represents the empty tile):")
        state = []
        for i in range(3):
            row = input(f"Enter row {i+1}: ").split()
            if len(row) != 3:
                print("Invalid input. Please enter 3 numbers per row.")
                continue
            try:
                row = [int(x) for x in row]
            except ValueError:
                print("Invalid input. Please enter only numbers.")
                continue
            if not all(0 <= x <= 8 for x in row):
                print("Numbers must be between 0 and 8.")
                continue
            state.append(row)

        if len(set(sum(state, []))) != 9:
            print("Each number from 0 to 8 must appear exactly once.")
            continue

        return state

def main():
    start_state = get_user_input()
    solution = a_star_search(start_state)

    if solution:
        print("Solution found in", len(solution) - 1, "steps:")
        for step in solution:
            for row in step:
                print(row)
            print()
    else:
        print("No solution found.")
    print("Vanith D Ramesh (1BM22CS319)")

if __name__ == "__main__":
    main()