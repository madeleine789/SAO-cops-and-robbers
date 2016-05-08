import copy
import random
import math
from node import MCTSNode


class MCTreeSearch:
    def __init__(self, iterations_count, exploration=0.0):
        self.iterations_count = iterations_count
        self.exploration = exploration

    def perform_search_with_exploration(self, state, expl_param):
        self.exploration = expl_param
        root = MCTSNode(None, state, None)
        for i in xrange(self.iterations_count):
            self.perform_mcts_iteration(root, state.get_current_player())
        return self.get_promising_action(root)

    def perform_mcts_iteration(self, root, player):
        child = self.tree_policy(root)
        terminal_state = self.get_terminal_state(child, player)
        self.backpropagation(child, terminal_state)

    def get_terminal_state(self, node, player):
        cloned = copy.deepcopy(node.state)
        return player.get_to_terminal_state(cloned)

    def update_node_reward(self, node, state):
        parent_player = node.get_prev_player()
        node.update_reward(parent_player.get_reward_from_terminal_state(state))

    def backpropagation(self, node, state):
        while node is not None:
            self.update_node_reward(node, state)
            node = node.parent

    def tree_policy(self, node):
        # while not node.is_in_terminal_state():
        if len(node.state.get_available_actions_for_current_player()) == 0:
            return node.add_new_child_without_action()
        elif not node.is_node_expanded():
            return node.add_new_child_with_action(self.get_random_action(node))
        else:
            return max(node.children, key=self.compute_UCT)

    def get_random_action(self, node):
        return random.choice(node.get_not_used_actions_for_current_state())

    def get_promising_action(self, node):
        if len(node.children) > 0 and node.is_node_expanded() and not node.has_unknown_child():
            return max(node.children, key=node.get_bonus)
        else: return None

    def compute_UCT(self, node):
        return node.get_bonus() + self.exploration * math.sqrt(2 * math.log(node.parent.visit_count)) / node.visit_count
