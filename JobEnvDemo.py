from JobEnvironment import JobSchedulerEnv

if __name__ == "__main__":
    env = JobSchedulerEnv(render_mode="human")
    env.reset()

    # Use user input to control the environment as a human player (for testing)
    while True:
        action = int(input("Enter block: "))
        env.step(action)
        env.render()
        if env.model.game_over:
            print("Game Over!")
            break