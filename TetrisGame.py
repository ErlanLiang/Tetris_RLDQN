import pygame
import numpy as np

WIDTH = 10
HEIGHT = 22
BLOCK_SIZE = 30
Grid = np.zeros((HEIGHT, WIDTH), dtype=bool) # TODO: Replace with TetrisGrid class

GREY = (128, 128, 128)
PURPLE = (103, 80, 164)
WHITE = (255, 255, 255)

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Tetris")
    screen = pygame.display.set_mode((WIDTH * BLOCK_SIZE, HEIGHT * BLOCK_SIZE))
    clock = pygame.time.Clock()
    running = True

    frames_passed = 0
    score = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        # Draw the 10x22 grid of blocks on screen
        for x in range(WIDTH):
            for y in range(HEIGHT):
                if Grid[y][x]:
                    pygame.draw.rect(screen, PURPLE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                else:
                    pygame.draw.rect(screen, GREY, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, WHITE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

        if frames_passed % 10 == 0:
            score += 1
            found = False
            for y in range(HEIGHT):
                for x in range(WIDTH):
                    if not Grid[y][x]:
                        Grid[y][x] = True
                        found = True
                        break
                if found:
                    break
            if not found:
                Grid = np.zeros((HEIGHT, WIDTH), dtype=bool)

        pygame.display.set_caption(f"Tetris - Score: {score}")
        frames_passed += 1

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()