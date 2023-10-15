import pygame
from TetrisModel import TetrisModel, TetrisAction

class TetrisGame_1:
    BLOCK_SIZE = 30
    GREY = (128, 128, 128)
    PURPLE = (103, 80, 164)
    WHITE = (255, 255, 255)

    def __init__(self):
        self.model = TetrisModel()
        
        pygame.init()
        pygame.display.set_caption("Tetris")
        self.screen = pygame.display.set_mode((self.model.WIDTH * self.BLOCK_SIZE, self.model.HEIGHT * self.BLOCK_SIZE))
        self.clock = pygame.time.Clock()

        self.frames_passed = 0
        self.frames_per_game_tick = 60
        

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.model.executeMove(TetrisAction.LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.model.executeMove(TetrisAction.RIGHT)
                elif event.key == pygame.K_DOWN:
                    self.model.executeMove(TetrisAction.DOWN)
                elif event.key == pygame.K_UP:
                    self.model.executeMove(TetrisAction.ROTATE)
                elif event.key == pygame.K_SPACE:
                    self.model.executeMove(TetrisAction.DROP)
                elif event.key == pygame.K_z:
                    self.model.executeMove(TetrisAction.TRANSFORM)
        return True

    def game_tick(self):
        if self.frames_passed % self.frames_per_game_tick == 0:
            self.model.executeMove(TetrisAction.DOWN)
        self.frames_passed += 1

    def draw_game(self):
        self.screen.fill((0, 0, 0))
        current_grid = self.model.grid.grid

        # Draw the static grid
        for x in range(self.model.WIDTH):
            for y in range(self.model.HEIGHT):
                color = self.PURPLE if current_grid[y][x] else self.GREY
                pygame.draw.rect(self.screen, color, (x * self.BLOCK_SIZE, y * self.BLOCK_SIZE, self.BLOCK_SIZE, self.BLOCK_SIZE))
                pygame.draw.rect(self.screen, self.WHITE, (x * self.BLOCK_SIZE, y * self.BLOCK_SIZE, self.BLOCK_SIZE, self.BLOCK_SIZE), 1)

        # Draw the current piece
        for i in range(self.model.current_piece.shape.shape[0]):
            for j in range(self.model.current_piece.shape.shape[1]):
                if self.model.current_piece.shape[i][j]:
                    color = self.PURPLE
                    pygame.draw.rect(self.screen, color, ((self.model.current_x + j) * self.BLOCK_SIZE, (self.model.current_y + i) * self.BLOCK_SIZE, self.BLOCK_SIZE, self.BLOCK_SIZE))
                pygame.draw.rect(self.screen, self.WHITE, (x * self.BLOCK_SIZE, y * self.BLOCK_SIZE, self.BLOCK_SIZE, self.BLOCK_SIZE), 1)

        pygame.display.set_caption(f"Tetris - Score: {self.model.score}")
        self.frames_passed += 1

if __name__ == "__main__":
    game = TetrisGame_1()
    game.model.startGame()

    running = True
    while running:
        running = game.handle_events()
        game.game_tick()
        game.draw_game()
        pygame.display.flip()
        game.clock.tick(60)

    print(f"Game over! Score: {game.model.score}")
    pygame.quit()