from JobEnvironment import JobSchedulerEnv

if __name__ == "__main__":
    env = JobSchedulerEnv(render_mode="human")
    env.reset()

    # Use user input to control the environment as a human player (for testing)
    while True:
        try:
            print("Available actions:", env.get_available_actions())
            block = int(input("Enter block: "))
            delay = int(input("Enter delay: "))
            a, b, c, d = env.step((block, delay))
            print("Reward:", b)
            env.render()
        except ValueError:
            print("Invalid input. Please enter a number.")
        except Exception as e:
            print("An error occurred:", e)
        if env.model.game_over:
            print("Game Over!")
            break
