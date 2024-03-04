import random
from JobEnvironment import JobSchedulerEnv

if __name__ == "__main__":
    env = JobSchedulerEnv(render_mode="human")
    env.reset()

    # Use user input to control the environment as a human player (for testing)
    count = 1
    while True:
        available_actions = env.get_available_actions()
        action = random.choice(available_actions)
        env.step(action)
        env.render()
        if env.model.game_over:
            print(f"Game Over! This was the {count}th game.")
            if count % 10 == 0:
                input("Press Enter to continue...")
            env.reset()
            count += 1
