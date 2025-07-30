import pygame
import random

pygame.init()
WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30
COLS, ROWS = WIDTH // BLOCK_SIZE, HEIGHT // BLOCK_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()

# Define Tetrimino shapes
SHAPES = {
    'I': [[1, 1, 1, 1]],
    'O': [[1, 1], [1, 1]],
    'T': [[0, 1, 0], [1, 1, 1]],
    'S': [[0, 1, 1], [1, 1, 0]],
    'Z': [[1, 1, 0], [0, 1, 1]],
    'J': [[1, 0, 0], [1, 1, 1]],
    'L': [[0, 0, 1], [1, 1, 1]],
}
COLORS = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), (0,255,255), (255,165,0), (128,0,128)]

grid = [[(0, 0, 0) for _ in range(COLS)] for _ in range(ROWS)]

class Tetrimino:
    def __init__(self):
        self.shape = random.choice(list(SHAPES.values()))
        self.color = random.choice(COLORS)
        self.x = COLS // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        rotated = [list(row) for row in zip(*self.shape[::-1])]
        if self.valid(rotated):
            self.shape = rotated

    def valid(self, shape=None, dx=0, dy=0):
        shape = shape or self.shape
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    nx = self.x + x + dx
                    ny = self.y + y + dy
                    if nx < 0 or nx >= COLS or ny >= ROWS:
                        return False
                    if ny >= 0 and grid[ny][nx] != (0, 0, 0):
                        return False
        return True

    def lock(self):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell and self.y + y >= 0:
                    grid[self.y + y][self.x + x] = self.color

def clear_rows():
    global grid
    new_grid = [row for row in grid if any(cell == (0, 0, 0) for cell in row)]
    cleared = ROWS - len(new_grid)
    grid = [[(0, 0, 0)] * COLS for _ in range(cleared)] + new_grid

def draw_grid():
    for y in range(ROWS):
        for x in range(COLS):
            pygame.draw.rect(screen, grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(screen, (50, 50, 50), (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

def draw_piece(piece):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, piece.color, ((piece.x + x) * BLOCK_SIZE, (piece.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

# Game Loop
fall_time = 0
piece = Tetrimino()
run = True
while run:
    screen.fill((0, 0, 0))
    fall_time += clock.get_rawtime()
    clock.tick()

    if fall_time > 500:
        if piece.valid(dy=1):
            piece.y += 1
        else:
            piece.lock()
            clear_rows()
            piece = Tetrimino()
            if not piece.valid():
                print("Game Over")
                run = False
        fall_time = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and piece.valid(dx=-1):
                piece.x -= 1
            elif event.key == pygame.K_RIGHT and piece.valid(dx=1):
                piece.x += 1
            elif event.key == pygame.K_DOWN and piece.valid(dy=1):
                piece.y += 1
            elif event.key == pygame.K_UP:
                piece.rotate()

    draw_grid()
    draw_piece(piece)
    pygame.display.update()

pygame.quit()