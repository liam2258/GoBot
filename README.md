
# GoBot

A Go board game AI that makes decisions using a Monte Carlo tree search method. It includes a complete console implementation of Go and allows the user to play against the AI.


## Table of Contents

- [Deployment](#deployment)
- [Running Tests](#running-tests)
- [Methodology](#methodology)
  - [Monte Carlo Tree](#monte-carlo-tree)
## Deployment

This project can be run simply using the following

```bash
  python main.py
```


## Running Tests

This project makes use of the Pytest library for testing. It can be downloaded using the following:

```bash
  pip install pytest
```

Once intalled it can be run with the following:
```bash
  pytest
```

## Methodology

This project utilizes object oriented programming (OOP) for it's design methodology. The functionality for the Go game itself is encapsulated in the GoGame class, including all of the methods needed to play the game and attributes to track the state.

#### Monte Carlo Tree

The MonteCarloTree class is an implementation of the Monte Carlo Tree Search (MCTS) algorithm, which is a heuristic search algorithm used in decision-making processes, most notably in Artificial Intelligence (AI) applications such as game playing.

The MCTS algorithm consists of four steps, which are repeatedly executed until a computational budget is exhausted:

Selection: Starting at the root node, a child node is selected recursively until a leaf node is reached.

Expansion: If the leaf node is not a terminal node (i.e., it does not end the game), one of its children is added to the tree.

Simulation: A game is simulated to the end from the newly added node, using a default policy.

Backpropagation: The result of the game simulation is backpropagated up the tree, and the visit counts and values of the nodes on the path from the root to the leaf node are updated.

The best_move method in the MonteCarloTree class encapsulates these four steps.