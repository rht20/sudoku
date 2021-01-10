from random import randint, shuffle, sample


def is_board_full(board, n):
    for row in range(n):
        for col in range(n):
            if board[row][col] == 0:
                return False

    return True


def is_valid_move(board, n, cell, value):
    row = cell[0]
    col = cell[1]

    for j in range(n):
        if j != col and board[row][j] == value:
            return False

    for i in range(n):
        if i != row and board[i][col] == value:
            return False

    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if i != row and j != col and board[i][j] == value:
                return False

    return True


def get_conflicted_cells(board, n, cell, value):
    row = cell[0]
    col = cell[1]

    conflicted_cells = []

    for j in range(0, n):
        if j != col and board[row][j] == value:
            conflicted_cells.append((row, j))

    for i in range(0, n):
        if i != row and board[i][col] == value:
            conflicted_cells.append((i, col))

    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if i != row and j != col and board[i][j] == value:
                conflicted_cells.append((i, j))

    return conflicted_cells


def solve_sudoku(board, n, cell):
    row = cell[0]
    col = cell[1]

    if row == n - 1 and col == n:
        return True

    if col == n:
        return solve_sudoku(board, n, (row + 1, 0))

    if board[row][col]:
        return solve_sudoku(board, n, (row, col + 1))

    for i in range(1, 10):
        if is_valid_move(board, n, cell, i):
            board[row][col] = i
            if solve_sudoku(board, n, (row, col + 1)):
                return True
            board[row][col] = 0

    return False


def fill_board(board, n, number_list, cell):
    row = cell[0]
    col = cell[1]

    if row == n - 1 and col == n:
        return True

    if col == n:
        return fill_board(board, n, number_list, (row + 1, 0))

    shuffle(number_list)

    for value in number_list:
        if is_valid_move(board, n, cell, value):
            board[row][col] = value
            if fill_board(board, n, number_list, (row, col + 1)):
                return True
            board[row][col] = 0

    return False


def remove_cell_value(board, n):
    empties = int((n * n * 3) // 5)
    remove_cell_list = sample(range(n * n), empties)

    for cell in remove_cell_list:
        row = int(cell // n)
        col = cell % n
        board[row][col] = 0


def generate_puzzle():
    n = 9
    board = [[0 for _ in range(n)] for _ in range(n)]
    number_list = [i for i in range(1, n + 1)]

    fill_board(board, n, number_list, (0, 0))
    remove_cell_value(board, n)

    return board


def print_board(board):
    n = len(board)
    for i in range(n):
        print(board[i])


def main():
    board = generate_puzzle()
    n = len(board)

    print("Input:")
    print_board(board)
    print()

    solve_sudoku(board, n, (0, 0))
    print("Solution:")
    print_board(board)


# main()
