import random
from aetypes import Enum
from graph import Graph
from mcts.player import MCTSPlayer


class Player(MCTSPlayer):
    def __init__(self, is_cop=True, taxi_cards=0, bus_cards=0, underground_cards=0):
        self._position = None
        self.is_cop = is_cop
        self.taxi_cards = taxi_cards
        self.bus_cards = bus_cards
        self.underground_cards = underground_cards

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self._position = position

    def get_to_terminal_state(self, state):
        pass

    def get_card(self, transport):
        if transport == 'taxi':
            self.taxi_cards += 1
        if transport == 'bus':
            self.bus_cards += 1
        if transport == 'underground':
            self.underground_cards += 1

    def use_card(self, transport):
        if transport == 'taxi':
            self.taxi_cards -= 1
        if transport == 'bus':
            self.bus_cards -= 1
        if transport == 'underground':
            self.underground_cards -= 1

    def can_ride_taxi(self):
        return self.taxi_cards > 0

    def can_ride_bus(self):
        return self.bus_cards > 0

    def can_ride_underground(self):
        return self.underground_cards > 0


class Color(Enum):
    BLUE, RED, YELLOW, GREEN, PINK = range(5)


class Cop(Player):
    def __init__(self, color):
        Player.__init__(is_cop=True, taxi_cards=10, bus_cards=8, underground_cards=4)
        self.color = color

    def get_reward_from_terminal_state(self, terminal_state):
        if terminal_state.cops_won():
            return 1
        else:
            return 0

    def __eq__(self, other):
        if type(other) != Cop: return False
        return self.color == other.color

    def __repr__(self):
        return "{0} cop".format(self.color.name)


class Robber(Player):
    def __init__(self):
        Player.__init__(is_cop=False, taxi_cards=4, bus_cards=3, underground_cards=3)
        self.double_moves = 2
        self.black_fare_cards = 5

    def use_double_move(self):
        self.double_moves -= 1

    def use_black_fare_card(self):
        self.black_fare_cards -= 1

    def has_black_fare_cards(self):
        return self.black_fare_cards > 0

    def has_double_move(self):
        return self.double_moves > 0

    def get_reward_from_terminal_state(self, terminal_state):
        if terminal_state.robber_won():
            return 1
        else:
            return 0


POSSIBLE_POSITIONS = [0, 4, 8, 16]
POSSIBLE_STARTING_POSITIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
DISTANCE_TO_COP = [0.196, 0.671, 0.540, 0.384, 0.196]


class PlayersOnGraph:
    def __init__(self, players):
        self.graph = Graph()
        self.players = players
        self.current_player = 0
        self.current_positions = self.generate_starting_positions()
        self.robber_possible_locations = random.shuffle(POSSIBLE_POSITIONS)
        self.most_probable_robber_position = random.choice(self.robber_possible_locations)

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
