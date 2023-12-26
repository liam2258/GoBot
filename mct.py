import random
import math

class MonteCarloTree:
    def __init__(self, game):
        self.game = game
        self.root = Node(game=self.game)

    def best_move(self, iterations):
        """
        Determines the best move to make from the root node based on the results of multiple simulations.

        Parameters:
        iterations (int): The number of simulations to run.

        Returns:
        action: The action associated with the best child of the root node after all simulations are run.
        """
        for _ in range(iterations):
            node = self.select_node(self.root)
            simulation_result = self.simulate(node)
            self.backpropagate(node, simulation_result)

        return self.get_best_child(self.root).action

    def select_node(self, node):
        """
        Selects a node for simulation. If the node is not fully expanded, it expands the node.
        Otherwise, it selects the best child according to the UCT formula.

        Parameters:
        node (Node): The node from which to start the selection.

        Returns:
        Node: The selected node for the next simulation.
        """
        while not node.is_terminal():
            if not node.is_fully_expanded():
                return self.expand(node)
            else:
                node = self.get_best_child(node)
        return node

    def expand(self, node):
        """
        Expands the given node by creating a new child node for an untried action.
        If there are no untried actions, the node itself is returned.

        Parameters:
        node (Node): The node to expand.

        Returns:
        Node: The new child node, or the original node if there are no untried actions.
        """
        actions = node.untried_actions()
        
        # Check if there are available actions to choose from
        if actions:
            action = random.choice(actions)
            next_state = node.game.clone()
            next_state.make_move(*action)
            new_node = Node(game=next_state, action=action, parent=node)
            node.add_child(new_node)
            return new_node
        else:
            # If no actions are available, return the current node
            return node


    def simulate(self, node):
        """
        Runs a simulation from the given node until a terminal state is reached.
        At each step, a move is randomly selected from the valid moves.

        Parameters:
        node (Node): The node from which to start the simulation.

        Returns:
        float: The score value of the terminal game state.
        """
        state = node.game.clone()
        while not state.is_over:
            valid_moves = state.get_valid_moves()
            move = random.choice(valid_moves)
            state.make_move(*move)
        return self.get_simulation_result(state)

    def get_simulation_result(self, state):
        """
        Calculates the score value of the game state. 
        Assigns higher scores for larger margins of victory and lower scores for larger margins of defeat.

        Parameters:
        state (GameState): The game state to evaluate.

        Returns:
        float: The score value of the game state.
        """
        result = state.calculate_score()
        current_player = self.game.current_player

        if current_player == 'W':
            margin = result['W Score'] - result['B Score']
        else:
            margin = result['B Score'] - result['W Score']

        if margin > 0:
            return 1 + 0.1 * margin  # Assign higher score for larger margin of victory
        elif margin < 0:
            return 0.5 - 0.05 * abs(margin)  # Decrease score for higher margin of defeat
        else:
            return 0.5  # It's a tie


    def backpropagate(self, node, result):
        """
        Backpropagates the simulation result through the tree.
        Increments 'visits' by 1 and 'wins' by the result for the node and its ancestors.

        Parameters:
        node (Node): The node from which the simulation was run.
        result (float): The result of the simulation to backpropagate.

        Returns:
        None
        """
        while node is not None:
            node.visits += 1
            node.wins += result
            node = node.parent

    def get_best_child(self, node):
        """
        Selects the best child node using the Upper Confidence Bound for Trees (UCT) formula.
        This balances exploration and exploitation by favoring nodes with high average reward and low visit count.

        Parameters:
        node (Node): The parent node from which to select the best child.

        Returns:
        Node: The best child node according to the UCT formula.
        """
        children = node.children
        best_child = max(children,
                        key=lambda c: c.wins / c.visits + 
                        math.sqrt(2 * math.log(node.visits) 
                        / c.visits))
        return best_child


class Node:
    def __init__(self, game=None, action=None, parent=None):
        self.game = game
        self.action = action
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0

    def is_terminal(self):
        return self.game.is_over

    def is_fully_expanded(self):
        return len(self.children) == len(self.untried_actions())

    def untried_actions(self):
        if self.is_terminal():
            return []
        valid_moves = self.game.get_valid_moves()
        return [action for action in valid_moves if action not in [child.action for child in self.children]]

    def add_child(self, node):
        self.children.append(node)
