import pygame
import random

pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 500
BLOCK_SIZE = 25
BOARD_WIDTH, BOARD_HEIGHT = 10, 20
BOARD_OFFSET_X, BOARD_OFFSET_Y = 50, 50
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Shapes and their colors
SHAPES = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 1, 1],
     [1, 1, 0]],

    [[1, 1, 0],
     [0, 1, 1]],

    [[1, 0, 0],
     [1, 1, 1]],

    [[0, 0, 1],
     [1, 1, 1]],

    [[1, 1],
     [1, 1]],

    [[1, 1, 1, 1]]
]

SHAPES_COLORS = [
    (255, 165, 0),  # Orange
    (65, 105, 225),  # Royal Blue
    (0, 255, 0),  # Green
    (255, 0, 0),  # Red
    (128, 0, 128),  # Purple
    (0, 255, 255),  # Cyan
    (255, 255, 0)  # Yellow
]


class TetrisGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Tetris')
        self.clock = pygame.time.Clock()
        self.board = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
        self.current_piece = self.new_piece()
        self.x, self.y = BOARD_WIDTH // 2 - len(self.current_piece[0]) // 2, 0
        self.score = 0

    def new_piece(self):
        return random.choice(SHAPES)

    def draw_board(self):
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                if self.board[y][x]:
                    pygame.draw.rect(self.screen, SHAPES_COLORS[self.board[y][x] - 1],
                                     (BOARD_OFFSET_X + x * BLOCK_SIZE, BOARD_OFFSET_Y + y * BLOCK_SIZE,
                                      BLOCK_SIZE, BLOCK_SIZE))

    def draw_piece(self):
        shape_color = SHAPES_COLORS[SHAPES.index(self.current_piece)]
        for y in range(len(self.current_piece)):
            for x in range(len(self.current_piece[0])):
                if self.current_piece[y][x]:
                    pygame.draw.rect(self.screen, shape_color,
                                     (BOARD_OFFSET_X + (self.x + x) * BLOCK_SIZE,
                                      BOARD_OFFSET_Y + (self.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def is_collision(self):
        for y in range(len(self.current_piece)):
            for x in range(len(self.current_piece[0])):
                if self.current_piece[y][x] and (self.y + y >= BOARD_HEIGHT or
                                                 self.x + x < 0 or self.x + x >= BOARD_WIDTH or
                                                 self.board[self.y + y][self.x + x]):
                    return True
        return False

    def join_piece(self):
        shape_index = SHAPES.index(self.current_piece) + 1
        for y in range(len(self.current_piece)):
            for x in range(len(self.current_piece[0])):
                if self.current_piece[y][x]:
                    self.board[self.y + y][self.x + x] = shape_index

    def check_lines(self):
        lines_to_clear = []
        for y in range(BOARD_HEIGHT):
            if all(self.board[y]):
                lines_to_clear.append(y)

        for y in lines_to_clear:
            self.board.pop(y)
            self.board.insert(0, [0] * BOARD_WIDTH)
            self.score += 100

    def rotate_piece(self, piece):
        rows, cols = len(piece), len(piece[0])
        rotated_piece = [[0] * rows for _ in range(cols)]
        for y in range(rows):
            for x in range(cols):
                rotated_piece[x][rows - y - 1] = piece[y][x]
        return rotated_piece

    def run(self):
        time_since_last_drop = 0
        drop_speed = 500  # Lower value means faster falling, adjust as desired

        while True:
            self.clock.tick(60)  # Set the frame rate to 60 FPS

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.x -= 1
                        if self.is_collision():
                            self.x += 1
                    elif event.key == pygame.K_RIGHT:
                        self.x += 1
                        if self.is_collision():
                            self.x -= 1
                    elif event.key == pygame.K_DOWN:
                        self.y += 1
                        if self.is_collision():
                            self.y -= 1
                    elif event.key == pygame.K_UP:
                        rotated_piece = self.rotate_piece(self.current_piece)
                        if not self.is_collision_with_rotated(rotated_piece):
                            self.current_piece = rotated_piece

            time_since_last_drop += self.clock.get_rawtime()

            if time_since_last_drop > drop_speed:
                time_since_last_drop = 0

                if not self.is_collision():
                    self.y += 1
                else:
                    self.y -= 1  # Move the piece back up one step
                    self.join_piece()
                    self.check_lines()
                    self.current_piece = self.new_piece()
                    self.x, self.y = BOARD_WIDTH // 2 - len(self.current_piece[0]) // 2, 0
                    if self.is_collision():
                        pygame.quit()
                        return

            self.screen.fill(BLACK)
            self.draw_board()
            self.draw_piece()

            pygame.display.update()

    def is_collision_with_rotated(self, rotated_piece):
        for y in range(len(rotated_piece)):
            for x in range(len(rotated_piece[0])):
                if rotated_piece[y][x] and (self.y + y >= BOARD_HEIGHT or
                                            self.x + x < 0 or self.x + x >= BOARD_WIDTH or
                                            self.board[self.y + y][self.x + x]):
                    return True
        return False


if __name__ == '__main__':
    game = TetrisGame()
    game.run()
