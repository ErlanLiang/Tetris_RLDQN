import pygame
import JobModel
import JobUtils

SCREEN_SIZE = (1680, 900)

if __name__ == "__main__":
    # Initialize the Job model
    model = JobModel.ScheduleModel()
    model.start_game()

    # Initialize the pygame module
    pygame.init()
    pygame.display.set_caption("Job Scheduler")
    half_size = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1])
    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()

    # Set up game loop
    running = True

    # Game loop
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                running = False
            elif event.type == pygame.KEYDOWN:
                # Handle the key presses
                if event.key == pygame.K_RETURN:
                    model.execute_move(JobModel.ScheduleAction.COMMIT)
                elif event.key == pygame.K_SPACE:
                    model.execute_move(JobModel.ScheduleAction.PROGRESS)
                elif event.key == pygame.K_1:
                    model.execute_move(JobModel.ScheduleAction.BLOCK1)
                elif event.key == pygame.K_2:
                    model.execute_move(JobModel.ScheduleAction.BLOCK2)
                elif event.key == pygame.K_3:
                    model.execute_move(JobModel.ScheduleAction.BLOCK3)
                elif event.key == pygame.K_4:
                    model.execute_move(JobModel.ScheduleAction.BLOCK4)
                elif event.key == pygame.K_5:
                    model.execute_move(JobModel.ScheduleAction.BLOCK5)
                elif event.key == pygame.K_6:
                    model.execute_move(JobModel.ScheduleAction.BLOCK6)
                elif event.key == pygame.K_7:
                    model.execute_move(JobModel.ScheduleAction.BLOCK7)
                elif event.key == pygame.K_8:
                    model.execute_move(JobModel.ScheduleAction.BLOCK8)
                elif event.key == pygame.K_9:
                    model.execute_move(JobModel.ScheduleAction.BLOCK9)

        # Draw the background (light grey)
        screen.fill((200, 200, 200))

        # TODO: Draw the grid on the left side of the screen
        # flip the y axis to draw the grid from bottom to top
        flipped_grid = model.grid.grid[::-1]
        block_size = min(half_size[0] // model.grid.WIDTH, half_size[1] // model.grid.HEIGHT)
        for x in range(model.grid.WIDTH):
            for y in range(model.grid.HEIGHT):
                pygame.draw.rect(screen, JobUtils.get_color(flipped_grid[y][x]), (x * block_size, y * block_size, block_size, block_size))
                pygame.draw.rect(screen, (255, 255, 255), (x * block_size, y * block_size, block_size, block_size), 1)
        # Draw a red line for current time (counting from bottom of the grid)
        curr_time = JobModel.MAX_SETUP_TIME
        pygame.draw.line(screen, (255, 0, 0), (0, (model.grid.HEIGHT - curr_time) * block_size), (model.grid.WIDTH * block_size, (model.grid.HEIGHT - curr_time) * block_size), 2)
        # label the current time to the right of the red line
        font = pygame.font.Font(None, 36)
        text = font.render(f"Current Time: {model.curr_time}", True, (255, 0, 0))
        screen.blit(text, (model.grid.WIDTH * block_size, (model.grid.HEIGHT - curr_time) * block_size))

        # TODO: Draw 9 jobs from the job list on the right side of the screen (3x3 grid of grids)
        margin_for_text = 20
        starting_x = half_size[0]
        job_list = model.curr_job
        job_size = min(half_size[0] // 3, half_size[1] // 3)
        job_block_size = min(half_size[0] // 3 // model.grid.WIDTH, ((job_size - margin_for_text) // JobModel.MAX_JOB_HEIGHT))
        for i in range(3):
            for j in range(3):
                if i * 3 + j >= len(job_list):
                    break
                job = job_list[i * 3 + j]
                # Draw a border around the job block
                pygame.draw.rect(screen, (0, 0, 0), (j * job_size + starting_x, i * job_size, job_size, job_size), 1)
                # Label the job block
                font = pygame.font.Font(None, 28)
                text = font.render(f"{i*3 + j + 1} Job type: {job.name}", True, (0, 0, 0))
                screen.blit(text, (j * job_size + starting_x, i * job_size))
                # Draw the job block
                job_shape = job.fix_shape
                for x in range(job_shape.shape[1]):
                    for y in range(job_shape.shape[0]):
                        if job_shape[y][x]:
                            pygame.draw.rect(screen, JobUtils.get_color(job.id), ((j * job_size) + x * job_block_size + starting_x, (i * job_size) + y * job_block_size + margin_for_text, job_block_size, job_block_size))
                        pygame.draw.rect(screen, (255, 255, 255), ((j * job_size) + x * job_block_size + starting_x, (i * job_size) + y * job_block_size + margin_for_text, job_block_size, job_block_size), 1)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    print("Game Over")