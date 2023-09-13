import time
from collections import deque, namedtuple

import gym
import numpy as np
import PIL.Image
import tensorflow as tf
import torch.utils
import utils

from tensorflow import keras
from pyvirtualdisplay import Display
from keras import Sequential
from keras.layers import Dense, Input
from keras.losses import MSE
from keras.optimizers import Adam


MEMORY_SIZE = 100_000     # size of memory buffer
GAMMA = 0.995             # discount factor
ALPHA = 1e-3              # learning rate

env = gym.make("ALE/Tetris-v5", render_mode="rgb_array")
state_size = env.observation_space.shape
num_actions = env.action_space.n

print('State Shape:', state_size)
print('Number of actions:', num_actions)

# Select an action
action = 4
env.reset()
# Run a single time step of the environment's dynamics with the given action.
next_, reward, done, truncated, _ = env.step(action)
print(reward)
# Replace the `current_state` with the state after the action is taken
current_state = next_

model = Sequential([
    Input(shape=state_size),
    Dense(units=64, activation='relu'),
    Dense(units=64, activation='relu'),
    Dense(units=num_actions, activation='linear'),
])

target_model = Sequential([
    Input(shape=state_size),
    Dense(units=64, activation='relu'),
    Dense(units=64, activation='relu'),
    Dense(units=num_actions, activation='linear'),
])

optimizer = Adam(learning_rate=ALPHA)

print(model.summary())
print(target_model.summary())

experience = namedtuple("Experience", field_names=["state", "action", "reward",
                                                   "next_state", "done"])


def compute_loss(experiences, gamma, q_network, target_q_network):
    # Unpack the mini-batch of experience tuples
    states, actions, rewards, next_states, done_vals = experiences

    # Compute max Q^(s,a)
    max_qsa = tf.reduce_max(target_q_network(next_states), axis=-1)

    # Set y = R if episode terminates, otherwise set y = R + γ max Q^(s,a).
    y_targets = rewards + (gamma * max_qsa * (1 - done_vals))

    # Get the q_values
    q_values = q_network(states)
    q_values = tf.gather_nd(q_values, tf.stack([tf.range(q_values.shape[0]),
                                                tf.cast(actions, tf.int32)],
                                               axis=1))

    # Calculate the loss
    loss = MSE(y_targets, q_values)

    return loss


def agent_learn(experiences, gamma):
    """
    Updates the weights of the Q networks.

    Args:
      experiences: (tuple) tuple of ["state", "action", "reward", "next_state", "done"] namedtuples
      gamma: (float) The discount factor.

    """

    # Calculate the loss
    with tf.GradientTape() as tape:
        loss = compute_loss(experiences, gamma, model, target_model)

    # Get the gradients of the loss with respect to the weights.
    gradients = tape.gradient(loss, model.trainable_variables)

    # Update the weights of the q_network.
    optimizer.apply_gradients(zip(gradients, model.trainable_variables))

    # update the weights of target q_network
    utils.update_target_network(model, target_model)

start = time.time()

num_episodes = 2000
max_num_timesteps = 1000

total_point_history = []

num_p_av = 100    # number of total points to use for averaging
epsilon = 1.0     # initial ε value for ε-greedy policy

# Create a memory buffer D with capacity N
memory_buffer = deque(maxlen=MEMORY_SIZE)

target_model.set_weights(model.get_weights())

state = env.reset()
total_points = 0

# state_qn = np.expand_dims(state, axis=0)  # state needs to be the right shape for the q_network
# print("state_qn:", state_qn)
# # state_qn = np.asanyarray(state_qn).astype(np.float32)
# # state_qn = keras.backend.cast_to_floatx(state_qn)
# tf.convert_to_tensor(state_qn, dtype=tf.float32)
# q_values = model(state_qn)
# print(q_values)
# action = utils.get_action(q_values, epsilon)


