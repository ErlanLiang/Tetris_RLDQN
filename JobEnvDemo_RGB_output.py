from JobEnvironment import JobSchedulerEnv
import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    env = JobSchedulerEnv(render_mode="rgb_array")
    env.reset()

    # Draw the observation (RGB array) with matplotlib
    observation = env.render()
    fixed_observation = np.transpose(observation, (1, 0, 2))  # matplotlib expects (width, height, channels), not (height, width, channels)
    plt.imshow(fixed_observation)
    plt.show()
    
    # Use user input to control the environment as a human player (for testing)
    while True:
        try:
            print("Available actions:", env.get_available_actions())
            block = int(input("Enter block: "))
            delay = int(input("Enter delay: "))
            observation, reward, terminated, truncated = env.step((block, delay))

            # Draw the observation (RGB array) with matplotlib
            fixed_observation = np.transpose(observation, (1, 0, 2))  # matplotlib expects (width, height, channels), not (height, width, channels)
            plt.imshow(fixed_observation)
            plt.show()
        except ValueError:
            print("Invalid input. Please enter a number.")
        except Exception as e:
            print("An error occurred:", e)
        if env.model.game_over:
            print("Game Over!")
            break
