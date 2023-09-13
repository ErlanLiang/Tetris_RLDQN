import random
from collections import deque, namedtuple
import time

import test
from ale_py import ALEInterface
import gym
import numpy as np
import tensorflow as tf
import gymnasium
from tensorflow import keras
from keras import Sequential
from keras.layers import Dense, Input, Conv2D, Flatten
# from keras.losses import MeanSquaredError as MSE
from keras.optimizers import Adam
from IPython.display import clear_output

MEMORY_SIZE = 60000  # size of memory buffer
GAMMA = 0.995  # discount factor
ALPHA = 1e-3  # learning rate


def build_dqn_model(input_shape, output_shape):
    model = Sequential([
        Conv2D(32, kernel_size=(3, 3), activation='relu',
               input_shape=input_shape),
        Flatten(),
        Dense(units=64, activation='relu'),
        Dense(units=64, activation='relu'),
        Dense(units=output_shape, activation='linear'),
    ])
    return model


class Agent:
    def __init__(self, state, action_space):
        self.state = state
        self.action_space = action_space
        self.epsilon = 1.0
        self.discount = GAMMA
        self.learning_rate = Adam(learning_rate=ALPHA)
        self.mini_batch_size = 32
        self.memory_buffer = deque(maxlen=MEMORY_SIZE)
        self.model = build_dqn_model(state, action_space)
        self.target_model = build_dqn_model(state, action_space)

    def get_action(self, state):
        # return 2
        if np.random.rand() < self.epsilon:
            return random.randrange(self.action_space)

        state = np.expand_dims(state, axis=0)
        q_values = self.model.predict(state)
        re = np.argmax(q_values[0])
        print("next action: ", re)
        return re

    def mini_batch_replay(self):
        if len(self.memory_buffer) < self.mini_batch_size:
            return
        mini_batch = random.sample(self.memory_buffer, self.mini_batch_size)
        for state, action, reward, next_state, done in mini_batch:
            state = np.expand_dims(state, axis=0)  # Add batch_size dimension
            next_state = np.expand_dims(next_state,
                                        axis=0)  # Add batch_size dimension

            next_state = tf.convert_to_tensor(next_state)
            next_state = tf.cast(next_state, tf.float32)
            max_qsa = tf.reduce_max(self.target_model(next_state),
                                    axis=-1)  # Compute max Q^(s,a)
            y_targets = reward + (self.discount * max_qsa * (1 - done))
            # Bellman, Set y = R if episode terminates,
            # otherwise set y = R + γ max Q^(s,a).

            state = tf.convert_to_tensor(state)
            state = tf.cast(state, tf.float32)
            q_values = self.model(state)
            temp_a = np.reshape(action, (q_values.shape[0],))
            q_values = tf.gather_nd(q_values,
                                    tf.stack([tf.range(q_values.shape[0]),
                                              tf.cast(temp_a, tf.int32)],
                                             axis=1))
            # print("q_v2: ", q_values)
            # Calculate the loss
            loss = keras.losses.MSE(y_targets, q_values)
            if self.epsilon > 0.01:
                self.epsilon *= 0.998
            print("epsilon: ", self.epsilon)
            return loss
            # if done:
            #     target[0][action] = reward
            # else:
            #     future_reward = np.amax(self.target_model.predict(next_state)[0])
            #     target[0][action] = reward + self.discount * future_reward
            # print("target2: ", target)

            # self.model.fit(state, target, epochs=1, verbose=0)

    def update_target_network(self):
        for target_weights, q_net_weights in zip(
                agent.target_model.weights, agent.model.weights
        ):
            target_weights.assign(
                ALPHA * q_net_weights + (1.0 - ALPHA) * target_weights)


def train_agent(agent, env, num_episodes):
    max_num_timesteps = 1000
    total_point_history = []

    agent.target_model.set_weights(agent.model.get_weights())
    for episode in range(num_episodes):
        state, _ = env.reset()
        # print(state.shape)
        # state = np.reshape(state, [1, agent.state[0]])
        total_points = 0
         # debug use
        for t in range(max_num_timesteps):
            # print("new round")
            action = agent.get_action(state)
            # print(action)
            next_state, reward, done, _, _ = env.step(action)
            # next_state = np.reshape(next_state, [1, agent.state[0]])
            reward += 0.000001

            # Add reward based on the current status of the grid
            grid = get_grid(env.unwrapped.ale)
            print(grid)
            clear_output()
            

            

            agent.memory_buffer.append(
                (state, action, reward, next_state, done))
            state = next_state
            total_points += reward
            # print("tot_p: ", total_points)

            # check the RAM
            # data = env.unwrapped.ale.getRAM()[45:]
            # i = 0
            # for n in data:
            #     print(np.binary_repr(n, 8), end=" ")
            #     i += 1
            #     if i > 20:
            #         print()
            #         i = 0
            # print(f"t={t}")
            # print()

            if done:
                print("donnnnnnnnnnne")
                break

        print("\ntot_p: ", total_points)
        total_point_history.append(total_points)  # debug use
        av_latest_points = np.mean(total_point_history[-100:])
        print(f"\rEpisode {episode + 1} | Total point average of the last 100 "
              f"episodes: {av_latest_points:.2f}")
        # if episode == 1:
        #     time.sleep(10)
        #     return

        with tf.GradientTape() as tape:
            loss = agent.mini_batch_replay()
            # Get the gradients of the loss with respect to the weights.
            gradients = tape.gradient(loss, agent.model.trainable_weights)
        # Update the weights of the q_network.
        agent.learning_rate.apply_gradients(
            zip(gradients, agent.model.trainable_weights))
        agent.update_target_network()

        # agent.target_model.set_weights(agent.model.get_weights())

# Get Grid.
def to_bits(n):
    return [int(x) for x in np.binary_repr(n, 8)]

def get_grid(ale: ALEInterface) -> np.ndarray:
    grid = np.empty([22, 10], dtype=int)
    screen = ale.getRAM()[0:44]
    col = 0
    for i in range(22):
        cur = to_bits(screen[i])
        for y in range(2, 8):
            grid[i][col] = cur[y]
            col += 1
        col = 0
  
    for i in range(22):
        col = 6
        cur = to_bits(screen[i+22])
        for y in range(7, 3, -1):
            grid[i][col] = cur[y]
            col += 1
    return grid

if __name__ == "__main__":
    # gymnasium.make("ALE/Tetris-v5")
    env = gym.make("ALE/Tetris-v5", render_mode="human")
    s = env
    state_size = env.observation_space.shape
    num_actions = env.action_space.n

    ale: ALEInterface = env.unwrapped.ale
    
    agent = Agent(state_size, num_actions)
    # grid = get_grid(env.unwrapped.ale)
    
    num_episodes = 1000
    # print("obs space:", env.step(0)[0])
    train_agent(agent, env, num_episodes)

    # env.reset()
    # image = PIL.Image.fromarray(env.render())
    # image.show()
    #
    # gym.envs.registry.keys()
