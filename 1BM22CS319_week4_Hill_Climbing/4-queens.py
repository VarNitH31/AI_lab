import random

def hill_climbing_n_queens(n):
    board = generate_random_board(n)

    while True:
        current_cost = calculate_conflicts(board)
        if current_cost == 0:
            return board
        next_board, next_cost = get_best_neighbor(board)
        if next_cost >= current_cost:
            board = generate_random_board(n)
        else:

            board = next_board

def generate_random_board(n):

    return [random.randint(0, n - 1) for _ in range(n)]

def calculate_conflicts(board):

    conflicts = 0
    for i in range(len(board)):
        for j in range(i + 1, len(board)):
            if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                conflicts += 1
    return conflicts

def get_best_neighbor(board):
    n = len(board)
    best_board = board[:]
    best_cost = calculate_conflicts(board)
    for col in range(n):
        original_row = board[col]
        for row in range(n):
            if row != original_row:
                board[col] = row
                cost = calculate_conflicts(board)

                if cost < best_cost:
                    best_cost = cost
                    best_board = board[:]

        board[col] = original_row

    return best_board, best_cost

n=int(input("No of queens: "))  
solution = hill_climbing_n_queens(n)
print("Solution for", n, "queens:")
print(solution)

print("---------")
print("Vanith D Ramesh (1BM22CS319)")