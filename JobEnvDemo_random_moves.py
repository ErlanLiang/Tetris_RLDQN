import random
from JobEnvironment import JobSchedulerEnv

GAMES_PER_BATCH = 1

if __name__ == "__main__":
    env = JobSchedulerEnv(render_mode="human")
    env.reset()

    # Use user input to control the environment as a human player (for testing)
    count = 1
    while True:
        available_actions = env.get_available_actions()
        action = random.choice(available_actions)
        observation, reward, terminated, truncated = env.step(action)
        print("Reward:", reward)
        if terminated:
            print(f"Game Over! This was the {count}th game.", "Final reward:", env.model.total_reward)
            if count % GAMES_PER_BATCH == 0:
                input("Press Enter to continue...")
            env.reset()
            count += 1
