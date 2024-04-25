import pygame
import JobModel
import JobUtils

SCREEN_SIZE = (1680, 900)
DEBUG_SHOW_HIDDEN = False

def handle_key(key: int):
    global selection
    if key == 10:
        selection = None
        return
    if selection is None:
        selection = key
    else:
        global model
        if (selection, key) in model.get_available_actions():
            model.execute_move((selection, key))
        selection = None

if __name__ == "__main__":
    # Initialize the Job model
    model = JobModel.ScheduleModel()
    model.start_game()

    # Initialize the pygame module
    pygame.init()
    pygame.display.set_caption("Job Scheduler")
    top_text_margin = 20
    slot_size = (SCREEN_SIZE[0] // 10, SCREEN_SIZE[1] - top_text_margin)
    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()

    # Set up game loop
    running = True

    # Set up variables for user input
    selection = None

    # Game loop
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                running = False
            elif event.type == pygame.KEYDOWN:
                # Handle the key presses
                if event.key == pygame.K_SPACE:
                    model.execute_move((0, 0))
                elif event.key == pygame.K_0:
                    handle_key(0)
                elif event.key == pygame.K_1:
                    handle_key(1)
                elif event.key == pygame.K_2:
                    handle_key(2)
                elif event.key == pygame.K_3:
                    handle_key(3)
                elif event.key == pygame.K_4:
                    handle_key(4)
                elif event.key == pygame.K_5:
                    handle_key(5)
                elif event.key == pygame.K_6:
                    handle_key(6)
                elif event.key == pygame.K_7:
                    handle_key(7)
                elif event.key == pygame.K_8:
                    handle_key(8)
                elif event.key == pygame.K_9:
                    handle_key(9)
                elif event.key == pygame.K_r:   # Clear the selection
                    handle_key(10)

        # Draw the background (light grey)
        screen.fill((200, 200, 200))

        # Draw the grid on the left side of the screen
        # flip the y axis to draw the grid from bottom to top
        hidden_height = JobModel.max_setup_time
        grid_width = model.grid.WIDTH
        grid_height = model.grid.HEIGHT if DEBUG_SHOW_HIDDEN else model.grid.HEIGHT - hidden_height
        flipped_grid = model.grid.grid[::-1]
        block_size = min(slot_size[0] // grid_width, slot_size[1] // grid_height)
        for x in range(grid_width):
            for y in range(grid_height):
                pygame.draw.rect(screen, JobUtils.get_color(flipped_grid[y][x]), (x * block_size, y * block_size + top_text_margin, block_size, block_size))
                pygame.draw.rect(screen, (255, 255, 255), (x * block_size, y * block_size + top_text_margin, block_size, block_size), 1)
        # Draw a red line for current time if hidden part is shown (counting from bottom of the grid)
        if DEBUG_SHOW_HIDDEN:
            curr_time = hidden_height if DEBUG_SHOW_HIDDEN else 0
            pygame.draw.line(screen, (255, 0, 0), (0, (grid_height - curr_time) * block_size + top_text_margin), (grid_width * block_size, (grid_height - curr_time) * block_size + top_text_margin), 2)
        # label the current time
        font = pygame.font.Font(None, 24)
        status_text = f"Time: {model.base_time}"
        if selection is not None:
            status_text += f"|Chose {selection}"
        text = font.render(status_text, True, (255, 0, 0))
        screen.blit(text, (0, 0))

        # Draw 9 jobs from the job list on each slot
        job_list = model.job_list
        for i in range(9):
            starting_x = slot_size[0] * (i + 1)
            if i >= len(job_list):
                break
            job = job_list[i]
            # Label the job block
            font = pygame.font.Font(None, 24)
            text = font.render(f"{i + 1} Job type: {job.job_type}", True, (0, 0, 0))
            screen.blit(text, (starting_x, 0))
            # Draw the job block
            job_shape = job.rotated_shape
            for x in range(job_shape.shape[1]):
                for y in range(job_shape.shape[0]):
                    if job_shape[y][x]:
                        pygame.draw.rect(screen, JobUtils.get_color(job.id), (x * block_size + starting_x, y * block_size + top_text_margin, block_size, block_size))
                    else:
                        pygame.draw.rect(screen, JobUtils.get_color(0), (x * block_size + starting_x, y * block_size + top_text_margin, block_size, block_size))
                    pygame.draw.rect(screen, (255, 255, 255), (x * block_size + starting_x, y * block_size + top_text_margin, block_size, block_size), 1)
        if model.game_over:
            running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    print("Game Over")