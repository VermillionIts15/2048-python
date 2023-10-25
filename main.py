import pygame
import random
import time

pygame.init()

SCREEN_SIZE = 400
GRID_SIZE = 4
TILE_SIZE = SCREEN_SIZE // GRID_SIZE
WHITE = (255, 255, 255)
BACKGROUND = (187, 173, 160)
FONT_COLOR = (119, 110, 101)
SCORE_FONT_COLOR = (249, 246, 242)
SCORE_FONT_SIZE = 32
MENU_FONT_SIZE = 48

TILE_COLORS = {
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}

clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption('2048')

font = pygame.font.Font(None, MENU_FONT_SIZE)
game_over_font = pygame.font.Font(None, MENU_FONT_SIZE)
score_font = pygame.font.Font(None, SCORE_FONT_SIZE)
grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
animation_queue = []

def draw_rounded_rect(x, y, width, height, radius, color):
    rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, color, rect, border_radius=radius)


def draw_tile(x, y, value):
    if value == 0:
        return
    rect_x = x * TILE_SIZE
    rect_y = y * TILE_SIZE
    tile_color = TILE_COLORS.get(value, (128, 128, 128))
    text_color = FONT_COLOR if value <= 4 else SCORE_FONT_COLOR
    draw_rounded_rect(rect_x, rect_y, TILE_SIZE, TILE_SIZE, 10, tile_color)
    text_surface = font.render(str(value), True, text_color)
    text_rect = text_surface.get_rect(center=(rect_x + TILE_SIZE / 2, rect_y + TILE_SIZE / 2))
    screen.blit(text_surface, text_rect)


def draw_grid():
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            draw_tile(x, y, grid[y][x])


def move(direction):
    global grid
    if direction == 'up':
        for x in range(GRID_SIZE):
            merge_column_up(x)
    elif direction == 'down':
        for x in range(GRID_SIZE):
            merge_column_down(x)
    elif direction == 'left':
        for y in range(GRID_SIZE):
            merge_row_left(y)
    elif direction == 'right':
        for y in range(GRID_SIZE):
            merge_row_right(y)
    add_tile()


def animate_tile_movement(start_x, start_y, end_x, end_y, value):
    step = 0.1
    x, y = start_x, start_y

    while x != end_x or y != end_y:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.fill(BACKGROUND)
        draw_grid()
        draw_tile(x, y, value)
        pygame.display.flip()

        if x < end_x:
            x = min(x + step, end_x)
        elif x > end_x:
            x = max(x - step, end_x)

        if y < end_y:
            y = min(y + step, end_y)
        elif y > end_y:
            y = max(y - step, end_y)

        pygame.time.delay(10)

def process_animations():
    if animation_queue:
        animation = animation_queue[0]
        animation()
        animation_queue.pop(0)

def merge_column_up(x):
    for y in range(1, GRID_SIZE):
        if grid[y][x] != 0:
            for y2 in range(y - 1, -1, -1):
                if grid[y2][x] == 0:
                    grid[y2][x] = grid[y][x]
                    grid[y][x] = 0
                    animate_tile_movement(x, y, x, y2, grid[y2][x])
                    break
                elif grid[y2][x] == grid[y][x]:
                    grid[y2][x] *= 2
                    grid[y][x] = 0
                    animate_tile_movement(x, y, x, y2, grid[y2][x])
                    break

def merge_column_down(x):
    for y in range(GRID_SIZE - 2, -1, -1):
        if grid[y][x] != 0:
            for y2 in range(y + 1, GRID_SIZE):
                if grid[y2][x] == 0:
                    grid[y2][x] = grid[y][x]
                    grid[y][x] = 0
                    animate_tile_movement(x, y, x, y2, grid[y2][x])
                    break

def merge_row_left(y):
    for x in range(1, GRID_SIZE):
        if grid[y][x] != 0:
            for x2 in range(x - 1, -1, -1):
                if grid[y][x2] == 0:
                    grid[y][x2] = grid[y][x]
                    grid[y][x] = 0
                    animate_tile_movement(x, y, x2, y, grid[y][x2])
                    break

def merge_row_right(y):
    for x in range(GRID_SIZE - 2, -1, -1):
        if grid[y][x] != 0:
            for x2 in range(x + 1, GRID_SIZE):
                if grid[y][x2] == 0:
                    grid[y][x2] = grid[y][x]
                    grid[y][x] = 0
                    animate_tile_movement(x, y, x2, y, grid[y][x2])
                    break

def is_game_over():
    if all(grid[y][x] != 0 for y in range(GRID_SIZE) for x in range(GRID_SIZE)):
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                if (x < GRID_SIZE - 1 and grid[y][x] == grid[y][x + 1]) or (y < GRID_SIZE - 1 and grid[y][x] == grid[y + 1][x]):
                    return False
        return True
    return False

def has_won():
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if grid[y][x] == 2048:
                return True
    return False

def add_tile():
    empty_cells = [(x, y) for y in range(GRID_SIZE) for x in range(GRID_SIZE) if grid[y][x] == 0]
    if empty_cells:
        x, y = random.choice(empty_cells)
        grid[y][x] = 2 if random.random() < 0.9 else 4

def reset_game():
    global grid, game_over, win
    grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    game_over = False
    win = False
    add_tile()

points = 0

running = True
game_over = False
win = False

reset_game()

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_UP:
                move('up')
            elif event.key == pygame.K_DOWN:
                move('down')
            elif event.key == pygame.K_LEFT:
                move('left')
            elif event.key == pygame.K_RIGHT:
                move('right')

            if has_won():
                win = True

            game_over = is_game_over()
            points = sum(sum(row) for row in grid)

        if event.type == pygame.KEYDOWN and game_over and event.key == pygame.K_r:
            reset_game()

    screen.fill(BACKGROUND)

    # Process animations
    process_animations()

    draw_grid()

    points_text = score_font.render(f'Points: {points}', True, SCORE_FONT_COLOR)
    points_rect = points_text.get_rect(midtop=(SCREEN_SIZE // 2, 10))
    screen.blit(points_text, points_rect)

    if game_over:
        game_over_text = game_over_font.render("Game Over", True, FONT_COLOR)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_SIZE / 2, SCREEN_SIZE / 2))
        screen.blit(game_over_text, game_over_rect)

        restart_text = font.render("Press 'R' to restart", True, FONT_COLOR)
        restart_rect = restart_text.get_rect(center=(SCREEN_SIZE / 2, SCREEN_SIZE / 2 + 50))
        screen.blit(restart_text, restart_rect)

    if win:
        win_text = game_over_font.render("You Win!", True, FONT_COLOR)
        win_rect = win_text.get_rect(center=(SCREEN_SIZE / 2, SCREEN_SIZE / 2))
        screen.blit(win_text, win_rect)

    pygame.display.flip()

pygame.quit()
