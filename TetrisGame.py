import pygame
import numpy as np
from TetrisModel import TetrisModel
from TetrisModel import TetrisAction

BLOCK_SIZE = 30
GREY = (128, 128, 128)
PURPLE = (103, 80, 164)
WHITE = (255, 255, 255)
MODEL: TetrisModel

if __name__ == "__main__":

    # Initialize the Tetris model
    MODEL = TetrisModel()

    # Initialize the pygame module
    pygame.init()
    pygame.display.set_caption("Tetris")
    screen = pygame.display.set_mode((MODEL.WIDTH * BLOCK_SIZE, MODEL.HEIGHT * BLOCK_SIZE))
    clock = pygame.time.Clock()

    # Set up game loop
    running = True
    frames_passed = 0
    frames_per_game_tick = 30
    MODEL.startGame()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        MODEL.executeMove(TetrisAction.DOWN)

        screen.fill((0, 0, 0))

        # Draw the grid on screen
        for x in range(MODEL.WIDTH):
            for y in range(MODEL.HEIGHT):
                if MODEL.grid.Grid[y][x]:
                    pygame.draw.rect(screen, PURPLE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                else:
                    pygame.draw.rect(screen, GREY, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, WHITE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

        pygame.display.set_caption(f"Tetris - Score: {MODEL.score}")
        frames_passed += 1

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()