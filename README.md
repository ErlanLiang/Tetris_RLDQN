# Job Scheduler Usage 

## File Structure 

- JobModel.py: 

  Handles the game logic. 

- JobGame.py: 

  The human playable version of the game. 

- JobEnvironment.py: 

  The file with the class that implements the OpenAI Gymnasium API. 

- JobEnvDemo.py and JobEnvDemo_RGB_output.py: 

  Demo files that use user input to interact with the environment. 

- JobEnvDemo_random_moves.py: 

  A demo that uses random inputs to interact with the environment, mimics the usage of the environment class in a training set up.

## Running the Game

**Pre-requisites:** Python 3.9-3.11, with `pygame` and `numpy` packages.

```shell
# To install pygame and numpy, run the following command
pip install pygame numpy
```

To run the Gymnasium environment, the `gymnasium` package is required. 

```shell
# To install gymnasium, run the following command
pip install gym
```

**Starting the game:** Run `JobGame.py` to start the game. 

## Movement 

- **space** : Advance time by 1.
- **1-9**: Choose a block or delay time. 
- ​**r**: Reset block choice.
