import random
from mcts.player import MCTSPlayer


class Player(MCTSPlayer):
    def __init__(self, is_cop=True):
        self._position = None
        self.is_cop = is_cop

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self._position = position

    def get_reward_from_terminal_state(self, terminal_state):
        pass

    def get_to_terminal_state(self, state):
        pass


class Cop(Player):
    pass


class Robber(Player):
    pass


POSSIBLE_POSITIONS = [0, 4, 8, 16]
POSSIBLE_STARTING_POSITIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
DISTANCE_TO_COP = [0.196, 0.671, 0.540, 0.384, 0.196]


class PlayersOnGraph:
    def __init__(self, graph, players):
        self.graph = graph.init()
        self.players = players
        self.current_player = 0
        self.current_positions = self.generate_starting_positions()

    def generate_starting_positions(self):
        positions = set()
        for player in self.players:
            pos = random.choice(POSSIBLE_STARTING_POSITIONS)
            while pos in positions:
                pos = random.choice(POSSIBLE_STARTING_POSITIONS)
            positions.add(pos)
            player.position(pos)
        return positions

    def get_cops_positions(self):
        positions = self.current_positions
        for player in self.players:
            if not player.is_cop:
                positions.remove(player.position)
        return positions

    def get_robbers_positions(self):
        positions = self.current_positions
        for player in self.players:
            if not player.is_cop:
                positions.remove(player.position)
        return positions

    def generate_possible_robbers_locations(self):
        set(POSSIBLE_STARTING_POSITIONS).difference(self.get_cops_positions())

    def get_player_at_index(self, i):
        return self.players[i]

    def is_player_cop(self, i):
        return self.players[i].is_cop

    def is_player_robber(self, i):
        return not self.players[i].is_cop

    def cops_definitely_caught_robber(self):
        return False

    def cops_most_probably_caught_robber(self):
        return False
