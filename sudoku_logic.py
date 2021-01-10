from copy import deepcopy
from random import randint, shuffle, sample


def is_board_full(board, n):
    for row in range(n):
        for col in range(n):
            if board[row][col] == 0:
                return False

    return True


def is_valid(board, n, cell, value):
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
    column = cell[1]

    conflicted_cells = []

    for j in range(0, n):
        if j != column and board[row][j] == value:
            conflicted_cells.append((row, j))

    for i in range(0, n):
        if i != row and board[i][column] == value:
            conflicted_cells.append((i, column))

    start_row = (row // 3) * 3
    start_column = (column // 3) * 3
    for i in range(start_row, start_row + 3):
        for j in range(start_column, start_column + 3):
            if i != row and j != column and board[i][j] == value:
                conflicted_cells.append((i, j))

    return conflicted_cells


def fill_board(cell):
    row = cell[0]
    col = cell[1]

    if row == n - 1 and col == n:
        return True

    if col == n:
        return fill_board((row + 1, 0))

    global board, number_list

    shuffle(number_list)

    for value in number_list:
        if is_valid(board, n, cell, value):
            board[row][col] = value
            if fill_board((row, col + 1)):
                return True
            board[row][col] = 0

    return False


def solve_sudoku(cell):
    row = cell[0]
    col = cell[1]

    if row == n - 1 and col == n:
        return True

    if col == n:
        return solve_sudoku((row + 1, 0))

    if board[row][col]:
        return solve_sudoku((row, col + 1))

    for i in range(1, 10):
        if is_valid(board, n, cell, i):
            board[row][col] = i
            if solve_sudoku((row, col + 1)):
                return True
            board[row][col] = 0

    return False


def remove_cell_value():
    empties = int((n * n * 3) // 5)
    remove_cell_list = sample(range(n * n), empties)

    global board

    for cell in remove_cell_list:
        row = int(cell // n)
        col = cell % n
        board[row][col] = 0


def generate_puzzle():
    global n, board, number_list

    n = 9
    board = [[0 for _ in range(n)] for _ in range(n)]
    number_list = [i for i in range(1, n + 1)]

    fill_board((0, 0))

    remove_cell_value()

    copy_of_board = deepcopy(board)

    del n, board, number_list

    return copy_of_board


def print_board(board):
    for i in range(n):
        print(board[i])


def main():
    # board = [
    #     [3, 0, 6, 5, 0, 8, 4, 0, 0],
    #     [5, 2, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 8, 7, 0, 0, 0, 0, 3, 1],
    #     [0, 0, 3, 0, 1, 0, 0, 8, 0],
    #     [9, 0, 0, 8, 6, 3, 0, 0, 5],
    #     [0, 5, 0, 0, 9, 0, 6, 0, 0],
    #     [1, 3, 0, 0, 0, 0, 2, 5, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 7, 4],
    #     [0, 0, 5, 2, 0, 6, 3, 0, 0]
    # ]
    # n = len(board)

    board = generate_puzzle()
    n = len(board)

    print("Input:")
    print_board(board)
    print()

    solve_sudoku((0, 0))
    print("Solution:")
    print_board(board)


# main()
