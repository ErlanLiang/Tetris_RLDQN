import pygame
import JobModel
import JobUtils

SCREEN_SIZE = (1680, 900)

if __name__ == "__main__":
    # Initialize the Job model
    model = JobModel.ScheduleModel()

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
                    model.executeMove(JobModel.ScheduleAction.COMMIT)
                elif event.key == pygame.K_SPACE:
                    model.executeMove(JobModel.ScheduleAction.PROGRESS)
                elif event.key == pygame.K_1:
                    model.executeMove(JobModel.ScheduleAction.BLOCK1)
                elif event.key == pygame.K_2:
                    model.executeMove(JobModel.ScheduleAction.BLOCK2)
                elif event.key == pygame.K_3:
                    model.executeMove(JobModel.ScheduleAction.BLOCK3)
                elif event.key == pygame.K_4:
                    model.executeMove(JobModel.ScheduleAction.BLOCK4)
                elif event.key == pygame.K_5:
                    model.executeMove(JobModel.ScheduleAction.BLOCK5)
                elif event.key == pygame.K_6:
                    model.executeMove(JobModel.ScheduleAction.BLOCK6)
                elif event.key == pygame.K_7:
                    model.executeMove(JobModel.ScheduleAction.BLOCK7)
                elif event.key == pygame.K_8:
                    model.executeMove(JobModel.ScheduleAction.BLOCK8)
                elif event.key == pygame.K_9:
                    model.executeMove(JobModel.ScheduleAction.BLOCK9)

        # Draw the background (light grey)
        screen.fill((200, 200, 200))

        # TODO: Draw the grid on the left side of the screen
        block_size = min(half_size[0] // model.grid.WIDTH, half_size[1] // model.grid.HEIGHT)
        for x in range(model.grid.WIDTH):
            for y in range(model.grid.HEIGHT):
                pygame.draw.rect(screen, JobUtils.get_color(model.grid.grid[y][x]), (x * block_size, y * block_size, block_size, block_size))
                pygame.draw.rect(screen, (255, 255, 255), (x * block_size, y * block_size, block_size, block_size), 1)
        
        # TODO: Draw 9 jobs from the job list on the right side of the screen (3x3 grid)
        job_list = model.curr_job
        job_size = min(half_size[0] // 3, half_size[1] // 3)
        for i in range(3):
            for j in range(3):
                if i * 3 + j >= len(job_list):
                    break
                pygame.draw.rect(screen, JobUtils.get_color(job_list[i * 3 + j]), (half_size[0] + j * job_size, i * job_size, job_size, job_size))
                pygame.draw.rect(screen, (255, 255, 255), (half_size[0] + j * job_size, i * job_size, job_size, job_size), 1)


        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    print("Game Over")