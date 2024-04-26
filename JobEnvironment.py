import pygame
import JobModel
import JobUtils
import gymnasium as gym
import numpy as np

SCREEN_SIZE = (2560, 1440)   # Set the screen size for rendering, also used for size of grb_array
DEBUG_SHOW_HIDDEN = False   # Set to True to show the hidden part of the grid (for debugging)

class JobSchedulerEnv(gym.Env):
    model: JobModel.ScheduleModel
    action_space: gym.spaces.Discrete
    observation_space: gym.spaces.Box
    window: pygame.Surface
    clock: pygame.time.Clock

    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 10000}
    # The render_fps is set to a high value to make the rendering as fast as possible. 
    # The game loop will be controlled by the environment's step function, not the rendering.

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
        return self.render(), self.model.step_reward, self.model.game_over, None     # TODO: Currently returning the rendered state as the observation. Reward and info are None for now. Check if this is correct.

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
        top_text_margin = 20
        slot_size = (SCREEN_SIZE[0] // 10, SCREEN_SIZE[1] - top_text_margin)

        # Draw the grid on the left side of the screen
        # flip the y axis to draw the grid from bottom to top
        hidden_height = JobModel.max_setup_time
        grid_width = self.model.grid.WIDTH
        grid_height = self.model.grid.HEIGHT if DEBUG_SHOW_HIDDEN else self.model.grid.HEIGHT - hidden_height
        flipped_grid = self.model.grid.grid[::-1]
        block_size = min(slot_size[0] // grid_width - 1, slot_size[1] // grid_height)
        for x in range(grid_width):
            for y in range(grid_height):
                pygame.draw.rect(canvas, JobUtils.get_color(flipped_grid[y][x]), (x * block_size, y * block_size + top_text_margin, block_size, block_size))
                pygame.draw.rect(canvas, (255, 255, 255), (x * block_size, y * block_size + top_text_margin, block_size, block_size), 1)
        # Draw a red line for current time if hidden part is shown (counting from bottom of the grid)
        if DEBUG_SHOW_HIDDEN:
            curr_time = hidden_height if DEBUG_SHOW_HIDDEN else 0
            pygame.draw.line(canvas, (255, 0, 0), (0, (grid_height - curr_time) * block_size + top_text_margin), (grid_width * block_size, (grid_height - curr_time) * block_size + top_text_margin), 2)

        # label the current time
        font = pygame.font.Font(None, 24)
        text = font.render(f"Time: {self.model.base_time}", True, (255, 0, 0))
        canvas.blit(text, (0, 0))

        # Draw 9 jobs from the job list on each slot
        job_list = self.model.job_list
        for i in range(9):
            starting_x = slot_size[0] * (i + 1)
            if i >= len(job_list):
                break
            job = job_list[i]
            # Label the job block
            font = pygame.font.Font(None, 24)
            text = font.render(f"{i + 1} Job type: {job.job_type}", True, (0, 0, 0))
            canvas.blit(text, (starting_x, 0))
            # Draw the job block
            job_shape = job.rotated_shape
            for x in range(job_shape.shape[1]):
                for y in range(job_shape.shape[0]):
                    if job_shape[y][x]:
                        pygame.draw.rect(canvas, JobUtils.get_color(job.id), (x * block_size + starting_x, y * block_size + top_text_margin, block_size, block_size))
                    else:
                        pygame.draw.rect(canvas, JobUtils.get_color(0), (x * block_size + starting_x, y * block_size + top_text_margin, block_size, block_size))
                    pygame.draw.rect(canvas, (255, 255, 255), (x * block_size + starting_x, y * block_size + top_text_margin, block_size, block_size), 1)
        
        # Output the canvas
        if self.render_mode == "human":
            self.window.blit(canvas, canvas.get_rect())
            pygame.event.pump()
            pygame.display.flip()
            self.clock.tick(self.metadata["render_fps"])
        # Always return the canvas as rgb_array, even if the render_mode is "human"
        return np.transpose(pygame.surfarray.array3d(canvas), (1, 0, 2))

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()
            self.window = None
            self.clock = None

    def get_available_actions(self):
        return self.model.get_available_actions()