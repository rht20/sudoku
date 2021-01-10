import pygame
from time import time
from copy import deepcopy
from sudoku_logic import generate_puzzle, is_board_full, is_valid, get_conflicted_cells

pygame.init()


def initialize_board():
    global n, board, initial_board
    n = 9
    board = generate_puzzle()
    initial_board = deepcopy(board)


def setup_display():
    global display, display_height, display_width, display_color
    display_height = 550
    display_width = 800
    display_color = (60, 60, 60)

    display = pygame.display.set_mode((display_width, display_height))
    display.fill(display_color)
    pygame.display.set_caption("Sudoku")

    pygame.display.update()


def setup_variables():
    global sleep_time
    sleep_time = 100

    global start_time, finish_time, time_paused
    start_time = None
    finish_time = None
    time_paused = 0

    global font, btn_font
    font = pygame.font.SysFont('dejavuserif', 20)
    btn_font = pygame.font.SysFont('dejavuserif', 14)

    global black, white, red, gray, blue, btn_bg_color, btn_hover_bg_color
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    gray = (170, 170, 170)
    blue = (201, 233, 246)
    btn_bg_color = (70, 70, 70)
    btn_hover_bg_color = (80, 80, 80)

    global margin_top, margin_left
    margin_top = 50
    margin_left = 50

    global rect_height, rect_width
    rect_height = 50
    rect_width = 50

    global timer_margin_top, timer_margin_left, timer_height, timer_width
    timer_margin_top = 50
    timer_margin_left = (n * rect_width) + (2 * margin_left)
    timer_height = 50
    timer_width = 170

    global btn_margin_bottom, btn_margin_left, btn_gap
    btn_margin_bottom = 50
    btn_margin_left = (n * rect_width) + (2 * margin_left)
    btn_gap = 10

    global btn_height, btn_width
    btn_height = 60
    btn_width = 170

    global btn_text_list
    btn_text_list = ['Pause', 'Clear Board',
                     'New Puzzle', 'Visualize Solution']

    global current_selected_cell
    current_selected_cell = None

    global conflicted_cells, conflict_count
    conflicted_cells = {}
    conflict_count = {}


def get_bg_color(cell):
    row = cell[0]
    col = cell[1]

    if cell == current_selected_cell:
        return blue
    elif initial_board[row][col] != 0:
        return gray
    return white


def get_font_color(cell):
    return red if cell in conflict_count else black


def draw_cell(cell, bg_color):
    row = cell[0]
    col = cell[1]

    del_x = 2 if col % 3 == 0 else 1
    del_y = 2 if row % 3 == 0 else 1

    top_left_x = (col * rect_width) + margin_left + del_x
    top_left_y = (row * rect_height) + margin_top + del_y

    pygame.draw.rect(display, bg_color, (top_left_x,
                                         top_left_y, rect_width - del_x, rect_height - del_y))

    pygame.display.update()


def add_text(cell, value, font_color):
    value = int(value)
    if value == 0:
        return

    row = cell[0]
    col = cell[1]

    text_surface = font.render(str(value), True, font_color)
    text_rect = text_surface.get_rect()
    text_rect.center = ((col * rect_width) + margin_left + int(rect_width // 2),
                        (row * rect_height) + margin_top + int(rect_height // 2))
    display.blit(text_surface, text_rect)

    pygame.display.update()


def draw_grid():
    for row in range(0, n):
        for col in range(0, n):
            cell = (row, col)
            bg_color = get_bg_color(cell)
            font_color = get_font_color(cell)

            draw_cell(cell, bg_color)
            add_text(cell, board[row][col], font_color)


def draw_grid_borders():
    for row in range(0, n + 1):
        start_x = margin_left
        start_y = (row * rect_height) + margin_top
        end_x = (n * rect_width) + margin_left
        end_y = start_y

        thickness = 1
        if row % 3 == 0:
            thickness = 2

        pygame.draw.line(display, black,
                         (start_x, start_y), (end_x, end_y), thickness)

    for col in range(0, n + 1):
        start_x = (col * rect_width) + margin_left
        start_y = margin_top
        end_x = start_x
        end_y = (n * rect_height) + margin_top

        thickness = 1
        if col % 3 == 0:
            thickness = 2

        pygame.draw.line(display, black,
                         (start_x, start_y), (end_x, end_y), thickness)

    pygame.display.update()


def get_btn_coordinates(btn_id, total_btns):
    left_x = btn_margin_left
    top_y = (display_height - btn_margin_bottom - btn_height) - \
        ((total_btns - btn_id - 1) * (btn_height + btn_gap))
    right_x = left_x + btn_width
    bottom_y = top_y + btn_height

    return [(left_x, top_y), (right_x, bottom_y)]


def is_on_button(btn_coordinates, position):
    left_x = btn_coordinates[0][0]
    top_y = btn_coordinates[0][1]
    right_x = btn_coordinates[1][0]
    bottom_y = btn_coordinates[1][1]

    return left_x <= position[0] <= right_x and top_y <= position[1] <= bottom_y


def draw_button(btn_coordinates, btn_bg_color, btn_text):
    left_x = btn_coordinates[0][0]
    top_y = btn_coordinates[0][1]
    right_x = btn_coordinates[1][0]
    bottom_y = btn_coordinates[1][1]

    pygame.draw.rect(display, btn_bg_color,
                     (left_x, top_y, btn_width, btn_height))

    pygame.draw.line(display, black,
                     (left_x, top_y), (right_x, top_y), 1)
    pygame.draw.line(display, black,
                     (left_x, top_y), (left_x, bottom_y), 1)
    pygame.draw.line(display, black,
                     (left_x, bottom_y), (right_x, bottom_y), 1)
    pygame.draw.line(display, black,
                     (right_x, top_y), (right_x, bottom_y), 1)

    text_surface = btn_font.render(btn_text, True, white)
    text_rect = text_surface.get_rect()
    text_rect.center = (left_x + int(btn_width // 2),
                        top_y + int(btn_height // 2))
    display.blit(text_surface, text_rect)

    pygame.display.update()


def draw_buttons_and_handle_click():
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()

    for i in range(len(btn_text_list)):
        btn_coordinates = get_btn_coordinates(i, len(btn_text_list))

        if is_on_button(btn_coordinates, mouse_pos):
            draw_button(btn_coordinates, btn_hover_bg_color, btn_text_list[i])
            if mouse_click[0]:
                if i == 0:
                    pause()
                if i == 1:
                    clear_board()
                if i == 2:
                    new_puzzle()
                if i == 3:
                    initialize_timer()
                    solve_sudoku((0, 0))
                    global finish_time
                    finish_time = time()

        else:
            draw_button(btn_coordinates, btn_bg_color, btn_text_list[i])


def pause():
    pause_start_time = time()

    display.fill(display_color)
    pygame.display.update()

    left_x = int(display_width // 2) - int(btn_width // 2)
    top_y = int(display_height // 2) - int(btn_height // 2)
    right_x = left_x + btn_width
    bottom_y = top_y + btn_height

    btn_coordinates = [(left_x, top_y), (right_x, bottom_y)]

    while True:
        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()

            if is_on_button(btn_coordinates, mouse_pos):
                draw_button(btn_coordinates, btn_hover_bg_color, 'Resume')
                if mouse_click[0]:
                    pause_end_time = time()
                    time_elapsed = int(pause_end_time - pause_start_time)

                    global time_paused
                    time_paused += time_elapsed

                    resume()
                    return
            else:
                draw_button(btn_coordinates, btn_bg_color, 'Resume')


def resume():
    draw_grid()
    draw_grid_borders()
    draw_buttons_and_handle_click()


def clear_board():
    global current_selected_cell
    current_selected_cell = None

    global conflicted_cells, conflict_count
    conflicted_cells = {}
    conflict_count = {}

    global board
    board = deepcopy(initial_board)

    draw_grid()

    initialize_timer()


def new_puzzle():
    global board, initial_board

    board = generate_puzzle()
    initial_board = deepcopy(board)

    global current_selected_cell
    current_selected_cell = None

    global conflicted_cells, conflict_count
    conflicted_cells = {}
    conflict_count = {}

    draw_grid()

    initialize_timer()


def solve_sudoku(cell):
    show_timer()

    row = cell[0]
    col = cell[1]

    if row == n - 1 and col == n:
        return True

    if col == n:
        return solve_sudoku((row + 1, 0))

    if board[row][col] != 0:
        return solve_sudoku((row, col + 1))

    change_selected_cell(cell)
    # pygame.time.wait(sleep_time)

    for i in range(1, 10):
        show_timer()

        change_cell_value(cell, i)
        # pygame.time.wait(sleep_time)

        if is_valid(board, n, cell, i) == True:
            if solve_sudoku((row, col + 1)) == True:
                return True
            change_selected_cell(cell)

    change_cell_value(cell, 0)
    # pygame.time.wait(sleep_time)

    return False


def initialize_timer():
    global start_time, finish_time, time_paused
    start_time = time()
    finish_time = None
    time_paused = 0


def get_time_str():
    current_time = finish_time if finish_time != None else time()
    time_elapsed = int(current_time - start_time - time_paused)

    hours = int(time_elapsed // 3600)
    time_elapsed -= (hours * 3600)
    minutes = int(time_elapsed // 60)
    time_elapsed -= (minutes * 60)
    seconds = time_elapsed

    time_str = "Time: {0:02}:{1:02}:{2:02}".format(hours, minutes, seconds)

    return time_str


def show_timer():
    left_x = timer_margin_left
    top_y = timer_margin_top

    pygame.draw.rect(display, display_color,
                     (left_x, top_y, timer_width, timer_height))

    time_str = get_time_str()

    text_surface = font.render(time_str, True, white)
    text_rect = text_surface.get_rect()
    text_rect.center = (left_x + int(timer_width // 2),
                        top_y + int(timer_height // 2))
    display.blit(text_surface, text_rect)

    pygame.display.update()


def show_error():
    for cell in conflict_count:
        draw_cell(cell, get_bg_color(cell))
        add_text(cell, board[cell[0]][cell[1]], get_font_color(cell))


def recreate_conflict_free_cells(conflict_free_cells):
    for cell in conflict_free_cells:
        draw_cell(cell, get_bg_color(cell))
        add_text(cell, board[cell[0]][cell[1]], get_font_color(cell))


def get_selected_cell(position):
    top_left_x = margin_left
    top_left_y = margin_top
    bottom_right_x = (n * rect_width) + margin_left
    bottom_right_y = (n * rect_height) + margin_top

    cell = None
    if position[0] >= top_left_x and position[0] <= bottom_right_x and \
            position[1] >= top_left_y and position[1] <= bottom_right_y:
        col = int((position[0] - margin_left) // rect_width)
        row = int((position[1] - margin_top) // rect_height)
        cell = (row, col)

    return cell


def is_valid_cell(cell):
    if cell == None or not(cell[0] >= 0 and cell[0] < n) or not(cell[1] >= 0 and cell[1] < n):
        return False
    return True


def change_selected_cell(selected_cell):
    if not is_valid_cell(selected_cell):
        return

    global current_selected_cell

    prev_selected_cell = current_selected_cell
    current_selected_cell = selected_cell

    if prev_selected_cell != None:
        prev_row = prev_selected_cell[0]
        prev_col = prev_selected_cell[1]

        bg_color = get_bg_color(prev_selected_cell)
        font_color = get_font_color(prev_selected_cell)

        draw_cell(prev_selected_cell, bg_color)
        add_text(prev_selected_cell, board[prev_row][prev_col], font_color)

    cur_row = selected_cell[0]
    cur_col = selected_cell[1]

    bg_color = get_bg_color(current_selected_cell)
    font_color = get_font_color(current_selected_cell)

    draw_cell(current_selected_cell, bg_color)
    add_text(current_selected_cell, board[cur_row][cur_col], font_color)


def pre_update_conflicted_cells(cell):
    global conflicted_cells, conflict_count

    copy_of_conflicted_cells = deepcopy(conflicted_cells)
    conflict_free_cells = []

    if cell in copy_of_conflicted_cells:
        for item in copy_of_conflicted_cells[cell]:
            conflict_count[item] -= 1
            if conflict_count[item] == 0:
                conflict_count.pop(item)
                conflict_free_cells.append(item)

        conflicted_cells.pop(cell)
        conflict_count[cell] -= len(copy_of_conflicted_cells[cell])
        if conflict_count[cell] == 0:
            conflict_count.pop(cell)
            conflict_free_cells.append(cell)

    for key in copy_of_conflicted_cells:
        if cell in copy_of_conflicted_cells[key]:
            conflicted_cells[key].remove(cell)
            conflict_count[cell] -= 1
            if conflict_count[cell] == 0:
                conflict_count.pop(cell)
                conflict_free_cells.append(cell)

            conflict_count[key] -= 1
            if conflict_count[key] == 0:
                conflict_count.pop(key)
                conflict_free_cells.append(key)

            if len(conflicted_cells[key]) == 0:
                conflicted_cells.pop(key)

    recreate_conflict_free_cells(conflict_free_cells)


def post_update_conflicted_cells(cell, conflict_list):
    global conflicted_cells, conflict_count

    for item in conflict_list:
        conflict_count[item] = conflict_count.get(item, 0) + 1

    conflicted_cells[cell] = conflict_list
    conflict_count[cell] = conflict_count.get(cell, 0) + len(conflict_list)


def change_cell_value(cell, value):
    if not is_valid_cell(cell):
        return

    row = cell[0]
    col = cell[1]

    if initial_board[row][col] != 0 or board[row][col] == value:
        return

    pre_update_conflicted_cells(cell)

    board[row][col] = value

    draw_cell(cell, blue)
    add_text(cell, value, black)

    conflict_list = get_conflicted_cells(board, n, cell, value)
    if len(conflict_list) != 0:
        post_update_conflicted_cells(cell, conflict_list)
        show_error()


def handle_events():
    for event in pygame.event.get():
        draw_buttons_and_handle_click()

        if event.type == pygame.QUIT:
            global game_running
            game_running = False
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            position = pygame.mouse.get_pos()
            selected_cell = get_selected_cell(position)
            change_selected_cell(selected_cell)

        if event.type == pygame.KEYDOWN:
            value = -1
            direction = None

            if event.key == pygame.K_DELETE:
                value = 0

            if event.key == pygame.K_UP:
                direction = (-1, 0)
            if event.key == pygame.K_DOWN:
                direction = (1, 0)
            if event.key == pygame.K_LEFT:
                direction = (0, -1)
            if event.key == pygame.K_RIGHT:
                direction = (0, 1)

            if event.key == pygame.K_1:
                value = 1
            if event.key == pygame.K_2:
                value = 2
            if event.key == pygame.K_3:
                value = 3
            if event.key == pygame.K_4:
                value = 4
            if event.key == pygame.K_5:
                value = 5
            if event.key == pygame.K_6:
                value = 6
            if event.key == pygame.K_7:
                value = 7
            if event.key == pygame.K_8:
                value = 8
            if event.key == pygame.K_9:
                value = 9

            if direction != None and current_selected_cell != None:
                selected_cell = (
                    current_selected_cell[0] + direction[0], current_selected_cell[1] + direction[1])
                change_selected_cell(selected_cell)

            if value != -1:
                change_cell_value(current_selected_cell, value)


def game_loop():
    initialize_timer()

    global finish_time

    global game_running
    game_running = True

    while game_running:
        show_timer()

        if finish_time == None and is_board_full(board, n):
            finish_time = time()

        handle_events()


def main():
    initialize_board()
    setup_display()
    setup_variables()
    draw_grid_borders()
    draw_grid()
    draw_buttons_and_handle_click()
    game_loop()


main()
pygame.quit()
