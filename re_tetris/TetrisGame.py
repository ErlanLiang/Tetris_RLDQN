import pygame
import numpy as np
from TetrisModel import TetrisModel
from TetrisModel import TetrisAction

BLOCK_SIZE = 30
GREY = (128, 128, 128)
PURPLE = (103, 80, 164)
WHITE = (255, 255, 255)


if __name__ == "__main__":
    model: TetrisModel

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
    model.startGame()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    model.executeMove(TetrisAction.LEFT) 
                elif event.key == pygame.K_RIGHT:
                    model.executeMove(TetrisAction.RIGHT)
                elif event.key == pygame.K_DOWN:
                    model.executeMove(TetrisAction.DOWN)
                elif event.key == pygame.K_UP:
                    model.executeMove(TetrisAction.UP)
                elif event.key == pygame.K_SPACE:
                    model.executeMove(TetrisAction.DONESETUP)
                elif event.key == pygame.K_z:
                    model.executeMove(TetrisAction.PICK)

        # Execute default move every game_tick
        if not model.setup:
            if frames_passed % frames_per_game_tick == 0:
                model.executeMove(TetrisAction.DOWN)

        # Check if the game is over
        if model.game_over:
            running = False

        screen.fill((0, 0, 0))

        current_grid = model.grid.grid

        # Draw the grid on screen
        for x in range(model.WIDTH):
            for y in range(model.HEIGHT):
                if current_grid[y][x]:
                    pygame.draw.rect(screen, PURPLE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                else:
                    pygame.draw.rect(screen, GREY, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, WHITE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

        # Draw the current piece on top of the grid
        for i in range(model.current_piece.shape.shape[0]):
            for j in range(model.current_piece.shape.shape[1]):
                if model.current_piece.shape[i][j]:
                    pygame.draw.rect(screen, PURPLE, ((model.current_x + j) * BLOCK_SIZE, (model.current_y + i) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, WHITE, ((model.current_x + j) * BLOCK_SIZE, (model.current_y + i) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

        pygame.draw.rect(screen, WHITE, ((model.current_x + model.picker[1]) * BLOCK_SIZE, (model.current_y + model.picker[2]) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        pygame.display.set_caption(f"Tetris - Score: {model.score}")
        frames_passed += 1

        pygame.display.flip()
        clock.tick(60)

    print(f"Game over! Score: {model.score}")
    pygame.quit()