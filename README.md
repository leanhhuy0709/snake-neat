# Snake-NEAT

This repository contains an implementation of the classic game "Snake" using Python and the NeuroEvolution of Augmenting Topologies (NEAT) algorithm. The goal of this project is to train an AI to play Snake using genetic algorithms and neural networks.

## Files

- `main.py`: This script allows you to play the Snake game manually.
- `run_neat.py`: This script trains an AI to play the Snake game using the NEAT algorithm. The training configuration is specified in `config.py` and `config_neat.txt`.
- `run_winner.py`: This script visualizes the movements of the best-performing AI (the "winner") from the training process.
- `run_plot.py`: This script generates a plot showing the training progress of the winner.

## Usage

To play the Snake game manually, run:

```bash
python main.py
```

To train an AI to play the Snake game, run:
```bash
python run_neat.py
```

To visualize the movements of the winner, run:
```bash
python run_winner.py
```

To generate a plot of the training progress, run:
```bash
python run_plot.py
```

## Sources

This project was inspired by and based on the following resources:

- ["Game Development with Python - Snake using Pygame"](https://www.techwithtim.net/tutorials/game-development-with-python/snake-pygame/snake-tutorial-1) by Tech With Tim: This tutorial provided the base for the Snake game implementation.
- [NEAT-Python](https://neat-python.readthedocs.io/en/latest/): The Python library used for implementing the NEAT algorithm.