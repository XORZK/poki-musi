import pygame

CELL_SIZE = 40
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

BACKGROUND = BLACK
LINE_COLOR = WHITE

OFFSET = 10
FPS = 8

def color_map(v: int) -> tuple:
    match v:
        case 0:
            return BLACK
        case 1:
            return WHITE
        case 2:
            return RED
        case 3:
            return GREEN
        case 4:
            return BLUE
    return BLACK

def draw_square(x, y, color, screen):
    pygame.draw.rect(screen, color, (x * CELL_SIZE + OFFSET, y * CELL_SIZE + OFFSET, CELL_SIZE, CELL_SIZE))

def draw_grid(grid, screen):
    h,w = len(grid), len(grid[0])
    for y in range(0, h):
        for x in range(0, w):
            v = grid[y][x]
            color = color_map(v)
            draw_square(x,y,color,screen)

def draw_board(board, screen):
    h, w = len(board), len(board[0])
    for y in range(0, h):
        for x in range(0, w):
            color = board[y][x]
            draw_square(x,y,color,screen)


def draw_lines(screen, w, h):
    for x in range(0, w+1):
        pygame.draw.line(screen, LINE_COLOR, (x * CELL_SIZE + OFFSET, OFFSET), (x * CELL_SIZE + OFFSET, h * CELL_SIZE + OFFSET))
    for y in range(0, h+1):
        pygame.draw.line(screen, LINE_COLOR, (OFFSET, y * CELL_SIZE + OFFSET), (w * CELL_SIZE + OFFSET, y * CELL_SIZE + OFFSET))



