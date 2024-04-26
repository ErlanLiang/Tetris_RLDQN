from JobEnvironment import JobSchedulerEnv
import matplotlib.pyplot as plt

if __name__ == "__main__":
    env = JobSchedulerEnv(render_mode="rgb_array")
    env.reset()

    observation = env.render()

    # Draw the observation (RGB array) with matplotlib
    plt.imshow(observation)
    plt.show()
    
    # Use user input to control the environment as a human player (for testing)
    while True:
        try:
            print("Available actions:", env.get_available_actions())
            block = int(input("Enter block: "))
            delay = int(input("Enter delay: "))
            env.step((block, delay))
            observation = env.render()

            # Draw the observation (RGB array) with matplotlib
            plt.imshow(observation)
            plt.show()
        except ValueError:
            print("Invalid input. Please enter a number.")
        except Exception as e:
            print("An error occurred:", e)
        if env.model.game_over:
            print("Game Over!")
            break
