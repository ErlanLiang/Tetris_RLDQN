import pygame
import JobModel
import JobUtils
import gymnasium as gym
import numpy as np

SCREEN_SIZE = (1280, 720)
DEBUG_SHOW_HIDDEN = True

# TODO: Port JobGame to gym environment
class JobSchedulerEnv(gym.Env):
    model: JobModel.ScheduleModel
    action_space: gym.spaces.Discrete
    observation_space: gym.spaces.Box
    window: pygame.Surface
    clock: pygame.time.Clock

    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 30}

    def __init__(self, render_mode="human"):
        # Initialize the Job model
        self.model = JobModel.ScheduleModel()
        self.model.start_game()
        action_space_size = self.model.get_action_space_size()
        grid_shape = self.model.grid.grid.shape
        self.window = None
        self.clock = None

        # Set up the gym environment
        self.render_mode = render_mode
        self.action_space = gym.spaces.Discrete(action_space_size)                              # TODO: Check if this is the correct way to define the action space
        self.observation_space = gym.spaces.Box(low=0, high=1, shape=grid_shape, dtype=int)     # TODO: Check if this is the correct way to define the observation space

    def step(self, action: tuple[int, int]):
        self.model.execute_move(action)
        return self.render(), None, self.model.game_over, None     # TODO: Currently returning the rendered state as the observation. Reward and info are None for now. Check if this is correct.

    def reset(self, seed=None):
        super().reset(seed=seed)
        self.model = JobModel.ScheduleModel()
        self.model.start_game()
        return self.render(), None      # TODO: Currently returning the rendered state as the observation. Info is None for now. Check if this is correct.

    def render(self):
        pygame.init()
        # Initialize the pygame module
        if self.window is None and self.render_mode == "human":
            self.window = pygame.display.set_mode(SCREEN_SIZE)
            pygame.display.set_caption("Job Scheduler")
        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()
        
        # Create and draw on the canvas
        canvas = pygame.Surface(SCREEN_SIZE)
        canvas.fill((200, 200, 200))
        half_size = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1])

        # Draw the grid on the left side of the canvas
        # flip the y axis to draw the grid from bottom to top
        hidden_height = JobModel.max_setup_time
        grid_width = self.model.grid.WIDTH
        grid_height = self.model.grid.HEIGHT if DEBUG_SHOW_HIDDEN else self.model.grid.HEIGHT - hidden_height
        flipped_grid = self.model.grid.grid[::-1]
        block_size = min(half_size[0] // grid_width, half_size[1] // grid_height)
        for x in range(grid_width):
            for y in range(grid_height):
                pygame.draw.rect(canvas, JobUtils.get_color(flipped_grid[y][x]), (x * block_size, y * block_size, block_size, block_size))
                pygame.draw.rect(canvas, (255, 255, 255), (x * block_size, y * block_size, block_size, block_size), 1)
        # Draw a red line for current time if hidden part is shown (counting from bottom of the grid)
        if DEBUG_SHOW_HIDDEN:
            curr_time = hidden_height if DEBUG_SHOW_HIDDEN else 0
            pygame.draw.line(canvas, (255, 0, 0), (0, (grid_height - curr_time) * block_size), (grid_width * block_size, (grid_height - curr_time) * block_size), 2)
        # label the current time
        font = pygame.font.Font(None, 36)
        text = font.render(f"Current Time: {self.model.base_time}", True, (255, 0, 0))
        canvas.blit(text, (grid_width * block_size, 0))

        # Draw 9 jobs from the job list on the right side of the canvas (3x3 grid of grids)
        margin_for_text = 20
        starting_x = half_size[0]
        job_list = self.model.job_list
        job_size = min(half_size[0] // 3, half_size[1] // 3)
        job_block_size = min(half_size[0] // 3 // grid_width, ((job_size - margin_for_text) // JobModel.max_job_height))
        for i in range(3):
            for j in range(3):
                if i * 3 + j >= len(job_list):
                    break
                job = job_list[i * 3 + j]
                # Draw a border around the job block
                pygame.draw.rect(canvas, (0, 0, 0), (j * job_size + starting_x, i * job_size, job_size, job_size), 1)
                # Label the job block
                font = pygame.font.Font(None, 28)
                text = font.render(f"{i*3 + j + 1} Job type: {job.job_type}", True, (0, 0, 0))
                canvas.blit(text, (j * job_size + starting_x, i * job_size))
                # Draw the job block
                job_shape = job.rotated_shape
                for x in range(job_shape.shape[1]):
                    for y in range(job_shape.shape[0]):
                        if job_shape[y][x]:
                            pygame.draw.rect(canvas, JobUtils.get_color(job.id), ((j * job_size) + x * job_block_size + starting_x, (i * job_size) + y * job_block_size + margin_for_text, job_block_size, job_block_size))
                        pygame.draw.rect(canvas, (255, 255, 255), ((j * job_size) + x * job_block_size + starting_x, (i * job_size) + y * job_block_size + margin_for_text, job_block_size, job_block_size), 1)
        
        # Output the canvas
        if self.render_mode == "human":
            self.window.blit(canvas, canvas.get_rect())
            pygame.event.pump()
            pygame.display.flip()
            self.clock.tick(self.metadata["render_fps"])
        else:  # self.render_mode == "rgb_array"
            return np.transpose(pygame.surfarray.array3d(canvas), (1, 0, 2))

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()
            self.window = None
            self.clock = None

    def get_available_actions(self):
        return self.model.get_available_actions()