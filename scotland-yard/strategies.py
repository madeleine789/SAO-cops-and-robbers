import random


class Strategy:
    def __init__(self, used):
        self.used = used


class CoalitionReduction(Strategy):
    parameter = 0.2

    def __init__(self, used=False):
        Strategy.__init__(self, used)

    def get_reward_from_terminal_state(self, terminal_state, cop):
        if terminal_state.cop_won(cop):
            return 1
        if terminal_state.cops_won():
            return 1 - CoalitionReduction.parameter
        else:
            return 0


class MoveFiltering(Strategy):
    not_blackfare_rounds = [1,2,3,8,13,18,24]
    should_use_double_move_optimal_dist = 3
    should_use_double_mov_greedy = 0.3
    should_use_blackfare_greedy = 0.3

    def __init__(self, used=False):
        Strategy.__init__(self, used)

    @staticmethod
    def should_use_blackfare_optimal(round, actions):
        return round not in MoveFiltering.not_blackfare_rounds and all(a.transport == 'taxi' for a in actions)

    @staticmethod
    def should_use_blackfare_greedy():
        return random.random < MoveFiltering.should_use_blackfare_greedy

    @staticmethod
    def should_use_double_move_optimal(players):
        return players.get_avg_distance_from_robber() <= MoveFiltering.should_use_double_move_optimal_dist

    @staticmethod
    def should_use_double_move_greedy():
        return random.random < MoveFiltering.should_use_double_move_greedy

class Playouts(Strategy):
    def __init__(self, used=False):
        Strategy.__init__(self, used)

    @staticmethod
    def get_random_action(state):
        pass

    @staticmethod
    def get_greedy_action_for_robber(state):
        pass

    @staticmethod
    def get_greedy_action_for_cop(state):
        pass