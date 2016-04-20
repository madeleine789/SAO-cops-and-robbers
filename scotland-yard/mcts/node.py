import copy


class MCTSNode:
    def __init__(self, parent, state, incoming_action):
        self.parent = parent
        self.state = state
        self.action = incoming_action
        self.visit_count = 0
        self.reward = 0.0
        self.children = []

    def has_children(self):
        return len(self.children) > 0

    def is_in_terminal_state(self):
        return self.state.is_terminal

    def has_unknown_child(self):
        return len(filter(lambda child: child.visit_count == 0, self.children)) == 0

    def is_node_expanded(self):
        return len(self.state.get_available_actions_for_current_player()) == len(self.children)

    def get_used_actions_for_current_state_and_player(self):
        return map(lambda child: child.action, self.children)

    def get_not_used_actions_for_current_state(self):
        return self.state.get_available_actions_for_current_player() - self.get_used_actions_for_current_state_and_player()

    def was_action_used(self, action):
        return action in self.get_used_actions_for_current_state_and_player()

    def add_new_child(self, current_state, incoming_action):
        child = MCTSNode(self, current_state, incoming_action)
        self.children.append(child)
        return child

    def add_new_child_with_action(self, action):
        if not self.was_action_used(action):
            state = self.get_new_state(action)
            child = MCTSNode(self, state, action)
            self.children.append(child)
            return child
        else: raise TypeError("Action has already been used")

    def add_new_child_without_action(self):
        state = copy.deepcopy(self.state)
        state.skip_current_player()
        child = MCTSNode(self, state, None)
        self.children.append(child)
        return child

    def update_reward(self, bonus):
        self.reward += bonus
        self.visit_count += 1

    def get_bonus(self):
        return self.visit_count / self.reward

    def get_new_state(self, action):
        state = copy.deepcopy(self.state)
        state.perform_action_for_current_player(action)
        return  state

    def get_prev_player(self):
        return self.state.get_prev_player()

