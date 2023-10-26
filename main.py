import pygame #ty pygame
import random

# Constants
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

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption('2048')
clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font(None, MENU_FONT_SIZE)
game_over_font = pygame.font.Font(None, MENU_FONT_SIZE)
score_font = pygame.font.Font(None, SCORE_FONT_SIZE)

class Game2048:
    def __init__(self):
        self.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.animation_queue = []
        self.points = 0
        self.game_over = False
        self.win = False

    def draw_rounded_rect(self, x, y, width, height, radius, color):
        # Function to draw rounded rectangles
        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, color, rect, border_radius=radius)

    def draw_tile(self, x, y, value):
        # Function to draw a single tile on the grid
        if value == 0:
            return
        rect_x = x * TILE_SIZE
        rect_y = y * TILE_SIZE
        tile_color = TILE_COLORS.get(value, (128, 128, 128))
        text_color = FONT_COLOR if value <= 4 else SCORE_FONT_COLOR
        self.draw_rounded_rect(rect_x, rect_y, TILE_SIZE, TILE_SIZE, 10, tile_color)
        text_surface = font.render(str(value), True, text_color)
        text_rect = text_surface.get_rect(center=(rect_x + TILE_SIZE / 2, rect_y + TILE_SIZE / 2))
        screen.blit(text_surface, text_rect)

    def draw_grid(self):
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                self.draw_tile(x, y, self.grid[y][x])

    def move(self, direction):
        if direction == 'up':
            for x in range(GRID_SIZE):
                self.merge_column_up(x)
        elif direction == 'down':
            for x in range(GRID_SIZE):
                self.merge_column_down(x)
        elif direction == 'left':
            for y in range(GRID_SIZE):
                self.merge_row_left(y)
        elif direction == 'right':
            for y in range(GRID_SIZE):
                self.merge_row_right(y)
        self.add_tile()

    def animate_tile_movement(self, start_x, start_y, end_x, end_y, value):
        step = 0.1
        x, y = start_x, start_y

        while x != end_x or y != end_y:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            screen.fill(BACKGROUND)
            self.draw_grid()
            self.draw_tile(x, y, value)
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

    def process_animations(self):
        if self.animation_queue:
            animation = self.animation_queue[0]
            animation()
            self.animation_queue.pop(0)

    def merge_column_up(self, x):
        for y in range(1, GRID_SIZE):
            if self.grid[y][x] != 0:
                for y2 in range(y - 1, -1, -1):
                    if self.grid[y2][x] == 0:
                        self.grid[y2][x] = self.grid[y][x]
                        self.grid[y][x] = 0
                        self.animation_queue.append(lambda x=x, y=y, x2=x, y2=y2, value=self.grid[y2][x]: self.animate_tile_movement(x, y, x2, y2, value))
                        break
                    elif self.grid[y2][x] == self.grid[y][x]:
                        self.grid[y2][x] *= 2
                        self.grid[y][x] = 0
                        self.animation_queue.append(lambda x=x, y=y, x2=x, y2=y2, value=self.grid[y2][x]: self.animate_tile_movement(x, y, x2, y2, value))
                        break

    def merge_column_down(self, x):
        for y in range(GRID_SIZE - 2, -1, -1):
            if self.grid[y][x] != 0:
                for y2 in range(y + 1, GRID_SIZE):
                    if self.grid[y2][x] == 0:
                        self.grid[y2][x] = self.grid[y][x]
                        self.grid[y][x] = 0
                        self.animation_queue.append(lambda x=x, y=y, x2=x, y2=y2, value=self.grid[y2][x]: self.animate_tile_movement(x, y, x2, y2, value))
                    elif self.grid[y2][x] == self.grid[y][x]:
                        self.grid[y2][x] *= 2
                        self.grid[y][x] = 0
                        self.animation_queue.append(lambda x=x, y=y, x2=x, y2=y2, value=self.grid[y2][x]: self.animate_tile_movement(x, y, x2, y2, value))
                        break

    def merge_row_left(self, y):
        for x in range(1, GRID_SIZE):
            if self.grid[y][x] != 0:
                for x2 in range(x - 1, -1, -1):
                    if self.grid[y][x2] == 0:
                        self.grid[y][x2] = self.grid[y][x]
                        self.grid[y][x] = 0
                        self.animation_queue.append(lambda x=x, y=y, x2=x2, y2=y, value=self.grid[y][x2]: self.animate_tile_movement(x, y, x2, y2, value))
                    elif self.grid[y][x2] == self.grid[y][x]:
                        self.grid[y][x2] *= 2
                        self.grid[y][x] = 0
                        self.animation_queue.append(lambda x=x, y=y, x2=x2, y2=y, value=self.grid[y][x2]: self.animate_tile_movement(x, y, x2, y2, value))
                        break

    def merge_row_right(self, y):
        for x in range(GRID_SIZE - 2, -1, -1):
            if self.grid[y][x] != 0:
                for x2 in range(x + 1, GRID_SIZE):
                    if self.grid[y][x2] == 0:
                        self.grid[y][x2] = self.grid[y][x]
                        self.grid[y][x] = 0
                        self.animation_queue.append(lambda x=x, y=y, x2=x2, y2=y, value=self.grid[y][x2]: self.animate_tile_movement(x, y, x2, y2, value))
                    elif self.grid[y][x2] == self.grid[y][x]:
                        self.grid[y][x2] *= 2
                        self.grid[y][x] = 0
                        self.animation_queue.append(lambda x=x, y=y, x2=x2, y2=y, value=self.grid[y][x2]: self.animate_tile_movement(x, y, x2, y2, value))
                        break

    def is_game_over(self):
        # Check if there are available moves
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                if self.grid[y][x] == 0:
                    return False
                if (x < GRID_SIZE - 1 and self.grid[y][x] == self.grid[y][x + 1]) or (y < GRID_SIZE - 1 and self.grid[y][x] == self.grid[y + 1][x]):
                    return False
        return True

    def has_won(self):
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                if self.grid[y][x] == 2048:
                    return True
        return False

    def add_tile(self):
        empty_cells = [(x, y) for y in range(GRID_SIZE) for x in range(GRID_SIZE) if self.grid[y][x] == 0]
        if empty_cells:
            x, y = random.choice(empty_cells)
            self.grid[y][x] = 2 if random.random() < 0.9 else 4

    def reset_game(self):
        self.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.game_over = False
        self.win = False
        self.add_tile()

game = Game2048()

while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN and not game.game_over:
            if event.key == pygame.K_UP:
                game.move('up')
            elif event.key == pygame.K_DOWN:
                game.move('down')
            elif event.key == pygame.K_LEFT:
                game.move('left')
            elif event.key == pygame.K_RIGHT:
                game.move('right')

            if game.has_won():
                game.win = True

            game.game_over = game.is_game_over()
            game.points = sum(sum(row) for row in game.grid)

        if event.type == pygame.KEYDOWN and game.game_over and event.key == pygame.K_r:
            game.reset_game()

    screen.fill(BACKGROUND)

    # Process animations
    game.process_animations()

    game.draw_grid()

    points_text = score_font.render(f'Points: {game.points}', True, SCORE_FONT_COLOR)
    points_rect = points_text.get_rect(midtop=(SCREEN_SIZE // 2, 10))
    screen.blit(points_text, points_rect)

    if game.game_over:
        game_over_text = game_over_font.render("Game Over", True, FONT_COLOR)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_SIZE / 2, SCREEN_SIZE / 2))
        screen.blit(game_over_text, game_over_rect)

        restart_text = font.render("Press 'R' to restart", True, FONT_COLOR)
        restart_rect = restart_text.get_rect(center=(SCREEN_SIZE / 2, SCREEN_SIZE / 2 + 50))
        screen.blit(restart_text, restart_rect)

    if game.win:
        win_text = game_over_font.render("You Win!", True, FONT_COLOR)
        win_rect = win_text.get_rect(center=(SCREEN_SIZE / 2, SCREEN_SIZE / 2))
        screen.blit(win_text, win_rect)

    pygame.display.flip()

pygame.quit()
