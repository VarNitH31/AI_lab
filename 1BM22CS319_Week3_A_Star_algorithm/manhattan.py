import heapq

GOAL_BOARD = [[2, 8, 1], [0, 4, 3], [7, 6, 5]]

MOVES = [(0, -1), (0, 1), (-1, 0), (1, 0)]

class PuzzleNode:
    def __init__(self, board, parent=None, g=0, h=0):
        self.board = board
        self.parent = parent
        self.g = g  
        self.h = h  
        self.f = g + h  

    def __lt__(self, other):
        return self.f < other.f

def manhattan_distance(board):
    distance = 0
    for i in range(3):
        for j in range(3):
            value = board[i][j]
            if value != 0:
                goal_x, goal_y = (value - 1) // 3, (value - 1) % 3
                distance += abs(i - goal_x) + abs(j - goal_y)
    return distance

def get_empty_tile(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                return i, j

def generate_neighbors(node):
    neighbors = []
    x, y = get_empty_tile(node.board)

    for dx, dy in MOVES:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < 3 and 0 <= new_y < 3:
            new_board = [row[:] for row in node.board]
            new_board[x][y], new_board[new_x][new_y] = new_board[new_x][new_y], new_board[x][y]
            h = manhattan_distance(new_board)
            neighbors.append(PuzzleNode(new_board, node, node.g + 1, h))

    return neighbors

def is_goal_reached(board):
    return board == GOAL_BOARD

def reconstruct_path(node):
    path = []
    while node:
        path.append(node.board)
        node = node.parent
    return path[::-1]

def a_star_search(start_board):
    open_set = [PuzzleNode(start_board)]
    closed_set = set()

    while open_set:
        current_node = heapq.heappop(open_set)

        if is_goal_reached(current_node.board):
            return reconstruct_path(current_node)

        closed_set.add(tuple(map(tuple, current_node.board)))

        for neighbor in generate_neighbors(current_node):
            if tuple(map(tuple, neighbor.board)) not in closed_set:
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