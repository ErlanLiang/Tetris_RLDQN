import pygame
import numpy as np
from TetrisModel import TetrisModel

BLOCK_SIZE = 30
GREY = (128, 128, 128)
PURPLE = (103, 80, 164)
WHITE = (255, 255, 255)

if __name__ == "__main__":
    # Initialize the Tetris model
    model = TetrisModel()

    # Initialize the pygame module
    pygame.init()
    pygame.display.set_caption("Tetris")
    screen = pygame.display.set_mode((model.WIDTH * BLOCK_SIZE, model.HEIGHT * BLOCK_SIZE))
    clock = pygame.time.Clock()

    # Set up game loop
    running = True
    frames_passed = 0
    frames_per_game_tick = 30

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        # Draw the grid on screen
        for x in range(model.WIDTH):
            for y in range(model.HEIGHT):
                if model.grid[y][x]:
                    pygame.draw.rect(screen, PURPLE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                else:
                    pygame.draw.rect(screen, GREY, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, WHITE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

        pygame.display.set_caption(f"Tetris - Score: {model.score}")
        frames_passed += 1

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()