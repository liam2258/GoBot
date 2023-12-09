import random
import math

class MonteCarloTree:
    def __init__(self, game):
        self.game = game
        self.root = Node(game=self.game)

    def best_move(self, iterations):
        for _ in range(iterations):
            node = self.select_node(self.root)
            simulation_result = self.simulate(node)
            self.backpropagate(node, simulation_result)

        return self.get_best_child(self.root).action

    def select_node(self, node):
        while not node.is_terminal():
            if not node.is_fully_expanded():
                return self.expand(node)
            else:
                node = self.get_best_child(node)
        return node

    def expand(self, node):
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
        state = node.game.clone()
        while not state.is_over:
            valid_moves = state.get_valid_moves()
            move = random.choice(valid_moves)
            state.make_move(*move)
        return self.get_simulation_result(state)

    def get_simulation_result(self, state):
        result = state.calculate_score()
        current_player = self.game.current_player

        if current_player == 'W':
            margin = result['W Score'] - result['B Score']
        else:
            margin = result['B Score'] - result['W Score']

        if margin > 0:
            return 1 + 0.1 * margin  # Assign higher score for larger margin of victory
        elif margin < 0:
            return 0.5 - 0.05 * abs(margin)  # Decrease score for smaller margin of defeat
        else:
            return 0.5  # It's a tie


    def backpropagate(self, node, result):
        while node is not None:
            node.visits += 1
            node.wins += result
            node = node.parent

    def get_best_child(self, node):
        children = node.children
        best_child = max(children, key=lambda c: c.wins / c.visits + math.sqrt(2 * math.log(node.visits) / c.visits))
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
