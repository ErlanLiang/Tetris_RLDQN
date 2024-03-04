from JobEnvironment import JobSchedulerEnv

if __name__ == "__main__":
    env = JobSchedulerEnv(render_mode="rgb_array")
    env.reset()

    # Use user input to control the environment as a human player (for testing)
    while True:
        try:
            block = int(input("Enter block: "))
            delay = int(input("Enter delay: "))
            env.step((block, delay))
            print(env.render())
        except ValueError:
            print("Invalid input. Please enter a number.")
        except Exception as e:
            print("An error occurred:", e)
        if env.model.game_over:
            print("Game Over!")
            break
