import random
import hardware
import numpy as np
import random

WIDTH = 16
HEIGHT = 12
TICK_TIME = 20

board = np.zeros(shape=(HEIGHT+1, WIDTH), dtype=tuple)
board.fill((0, 0, 0))

class Tetromino:
    def __init__(self, rotations, px = 6, py = 0, c = (255, 255, 255)):
        self.rotation_idx = 0
        self.rotations = rotations
        self.board = self.rotations[0]
        self.w = len(self.board[0])
        self.h = len(self.board)
        self.color = c
        self.pos = (px, py)
    def rotate_up(self):
        self.h, self.w = self.w, self.h
        self.rotation_idx = (self.rotation_idx + 1) % len(self.rotations)
        self.board = self.rotations[self.rotation_idx]
    def rotate_down(self):
        self.h, self.w = self.w, self.h
        self.rotation_idx = (self.rotation_idx - 1) % len(self.rotations)
        self.board = self.rotations[self.rotation_idx]

class I:
    rotations = [[[0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0]],
                 [[0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0]]]

class J:
    rotations = [[[1, 0, 0], [1, 1, 1], [0, 0, 0]],
                 [[0, 1, 1], [0, 1, 0], [0, 1, 0]],
                 [[0, 0, 0], [1, 1, 1], [0, 0, 1]],
                 [[0, 1, 0], [0, 1, 0], [1, 1, 0]]]

class L:
    rotations = [[[0, 0, 1], [1, 1, 1], [0, 0, 0]],
                 [[0, 1, 0], [0, 1, 0], [0, 1, 1]],
                 [[0, 0, 0], [1, 1, 1], [1, 0, 0]],
                 [[1, 1, 0], [0, 1, 0], [0, 1, 0]]]

class O:
    rotations = [[[0, 0, 0, 0], [0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]]]


class S:
    rotations = [[[0, 0, 0], [0, 1, 1], [1, 1, 0]], [[0, 1, 0], [0, 1, 1], [0, 0, 1]], [[0, 0, 0], [0, 1, 1], [1, 1, 0]], [[0, 1, 0], [0, 1, 1], [0, 0, 1]]]

class T:
    rotations = [[[0, 0, 0], [1, 1, 1], [0, 1, 0]], [[0, 1, 0], [1, 1, 0], [0, 1, 0]], [[0, 1, 0], [1, 1, 1], [0, 0, 0]], [[0, 1, 0], [0, 1, 1], [0, 1, 0]]]

class Z:
    rotations = [[[0, 0, 0], [1, 1, 0], [0, 1, 1]], [[0, 0, 1], [0, 1, 1], [0, 1, 0]], [[0, 0, 0], [1, 1, 0], [0, 1, 1]], [[0, 0, 1], [0, 1, 1], [0, 1, 0]]]

def clear_line(board, line):
    for x in range(WIDTH):
        board[line][x] = (0, 0, 0)

    for l in range(line, -1, -1):
        for x in range(WIDTH):
            board[l+1][x] = board[l][x]

    for x in range(WIDTH):
        board[HEIGHT][x] = (1, 1, 1)

def check_clear(board):
    for l in range(HEIGHT):
        cleared = True
        for x in range(WIDTH):
            if board[l][x] == (0, 0, 0):
                cleared = False
                break

        if (cleared):
            clear_line(board, l)

def game_over(board):
    for x in board[0]:
        if x != (0, 0, 0):
            return True
    return False

def random_tetromino():
    r = random.randint(0, 6)
    match r:
        case 0:
            return Tetromino(I.rotations, c = (173, 216, 230))
        case 1:
            return Tetromino(J.rotations, c = (0, 0, 220))
        case 2:
            return Tetromino(L.rotations, c = (0xFF, 0xA5, 0x00))
        case 3:
            return Tetromino(O.rotations, c = (255, 255, 0))
        case 4:
            return Tetromino(S.rotations, c = (0, 220, 0))
        case 5:
            return Tetromino(T.rotations, c = (160, 32, 240))
        case 6:
            return Tetromino(Z.rotations, c = (220, 0, 0))

def collides(board, curr_tet):
    for x in range(curr_tet.w):
        for y in range(curr_tet.h, 0, -1):
            if (curr_tet.board[y-1][x] == 1 and board[curr_tet.pos[1] + y][curr_tet.pos[0] + x] != (0, 0, 0)):
                return True

    return False

def draw_tetromino(hw, tet):
    for x in range(tet.w):
        for y in range(tet.h):
            if (tet.board[y][x] == 1):
                c = tet.color
                if (0 <= tet.pos[1] + y < HEIGHT and 0 <= tet.pos[0] + x < WIDTH):
                    hw.pixel[tet.pos[1] + y][tet.pos[0] + x] = (c[0] / 255, c[1] / 255, c[2] / 255)


def tick(hw, curr_tet):
    if (curr_tet is None):
        return

    draw_tetromino(hw, curr_tet)

    collided = collides(board, curr_tet)

    if collided:
        for x in range(curr_tet.w):
            for y in range(curr_tet.h):
                if (curr_tet.board[y][x] == 1):
                    board[curr_tet.pos[1] + y][curr_tet.pos[0] + x] = curr_tet.color

        curr_tet = random_tetromino()

    check_clear(board)

    return collided

def move_right(curr_tet, board):
    for x in range(curr_tet.w):
        for y in range(curr_tet.h):
            if (curr_tet.board[y][x] == 1 and (curr_tet.pos[0] + x + 1 >= WIDTH or board[curr_tet.pos[1] + y][curr_tet.pos[0] + x + 1] != (0, 0, 0))):
                return False

    return True

def move_left(curr_tet, board):
    for x in range(curr_tet.w):
        for y in range(curr_tet.h):
            if (curr_tet.board[y][x] == 1 and (curr_tet.pos[0] + x - 1 < 0 or board[curr_tet.pos[1] + y][curr_tet.pos[0] + x - 1] != (0, 0, 0))):
                return False
    return True

def can_rotate(curr_tet, board, up = True):
    shift = (1 if up else -1)

    rotated_board = curr_tet.rotations[(curr_tet.rotation_idx + shift) % len(curr_tet.rotations)]

    for x in range(curr_tet.h):
        for y in range(curr_tet.w):
            if (rotated_board[y][x] == 1 and (curr_tet.pos[0] + x < 0 or curr_tet.pos[0] + x >= WIDTH) or board[curr_tet.pos[1] + y][curr_tet.pos[0] + x] != (0, 0, 0)):
                return False

    return True

def fill_bg(hw, color: tuple):
    for k in range(WIDTH):
        for j in range(HEIGHT):
            hw.pixel[j][k] = color

def draw_board(hw):
    for y in range(HEIGHT):
        for x in range(WIDTH):
            c = board[y][x]
            hw.pixel[y][x] = (c[0] / 255, c[1] / 255, c[2] / 255)

def draw(hw, curr_tet):
    fill_bg(hw, (0, 0, 0))
    draw_board(hw)
    c = tick(hw, curr_tet)
    return c


def run(hw):
    lockout = 0
    max_lockout = 10
    r_movement = False
    h_movement = False
    board.fill((0, 0, 0))

    for x in range(WIDTH):
        board[HEIGHT][x] = (1, 1, 1)
    alive = True
    ticks = 0
    curr_tet = random_tetromino()

    while (alive):
        if (lockout == 0):
            if (hw.is_key_down(hardware.KEY_RIGHT)):
                if (move_right(curr_tet, board)):
                    curr_tet.pos = (curr_tet.pos[0] + 1, curr_tet.pos[1])
                    h_movement = True

                    c = draw(hw, curr_tet)
                    if (c): curr_tet = random_tetromino()
                    lockout = max_lockout
            elif (hw.is_key_down(hardware.KEY_LEFT)):
                if (move_left(curr_tet, board)):
                    curr_tet.pos = (curr_tet.pos[0] - 1, curr_tet.pos[1])
                    h_movement = True

                    c = draw(hw, curr_tet)
                    if (c): curr_tet = random_tetromino()
                    lockout = max_lockout
            elif (hw.is_key_down(hardware.KEY_UP)):
                if (can_rotate(curr_tet, board, True)):
                    curr_tet.rotate_up()
                    r_movement = True

                    c = draw(hw, curr_tet)
                    if (c): curr_tet = random_tetromino()
                    lockout = max_lockout
            elif (hw.is_key_down(hardware.KEY_DOWN)):
                if (can_rotate(curr_tet, board, False)):
                    curr_tet.rotate_up()
                    r_movement = True

                    c = draw(hw, curr_tet)
                    if (c): curr_tet = random_tetromino()
                    lockout = max_lockout
        else:
            if lockout > 0:
                lockout -= 1

        if (ticks % TICK_TIME == 0):
            if (lockout == 0):
                if (hw.is_key_down(hardware.KEY_UP)):
                    if (can_rotate(curr_tet, board, True)):
                        curr_tet.rotate_up()
                elif (hw.is_key_down(hardware.KEY_DOWN)):
                    if (can_rotate(curr_tet, board, False)):
                        curr_tet.rotate_up()

            fill_bg(hw, (0, 0, 0))
            draw_board(hw)
            c = tick(hw, curr_tet)
            if (c):
                curr_tet = random_tetromino()
            else:
                curr_tet.pos = (curr_tet.pos[0], curr_tet.pos[1] + 1)

        if (game_over(board)):
            alive = False

        ticks += 1

        hw.refresh()
