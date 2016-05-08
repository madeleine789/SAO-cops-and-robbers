import random
from aetypes import Enum
from graph import Graph
from mcts.player import MCTSPlayer
from action import Transport
from strategies import *


class Player(MCTSPlayer):
    def __init__(self, is_cop=True, taxi_cards=0, bus_cards=0, underground_cards=0, strategy=None):
        self.position = None
        self.is_cop = is_cop
        self.taxi_cards = taxi_cards
        self.bus_cards = bus_cards
        self.underground_cards = underground_cards
        self.strategy = strategy

    def get_to_terminal_state(self, state):
        while not state.is_terminal():
            action = self.get_action_for_current_player(state)
            if action is not None:
                state.perform_action_for_current_player(action)
            else:
                state.skip_current_player()
        return state

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

    def get_action_for_current_player(self, state):
        if state.players_on_graph.players[state.current_player].is_cop:
            return state.current_player.get_action_for_cop_from_simulation(state)
        return state.current_player.get_action_for_robber_from_simulation(state)

    def uses_coalition_reduction_strategy(self):
        cr = filter(lambda s: isinstance(s, CoalitionReduction), self.strategy)
        return len(cr) > 0

    def uses_move_filtering_strategy(self):
        mf = filter(lambda s: isinstance(s, MoveFiltering), self.strategy)
        return len(mf) > 0

    def uses_playouts_strategy(self):
        bp = filter(lambda s: isinstance(s, Playouts), self.strategy)
        return len(bp) > 0

    def get_action_for_cop_from_simulation(self, state):
        if self.uses_playouts_strategy():
            return Playouts.get_greedy_action_for_cop(state)
        else:
            return Playouts.get_random_action(state)

    def get_action_for_robber_from_simulation(self, state):
        if self.uses_playouts_strategy():
            return Playouts.get_greedy_action_for_robber(state)
        else:
            return Playouts.get_random_action(state)


class Color(Enum):
    BLUE, RED, YELLOW, GREEN, PINK = range(5)


class Cop(Player):
    def __init__(self, color, strategy):
        Player.__init__(self, is_cop=True, taxi_cards=10, bus_cards=8, underground_cards=4, strategy=strategy)
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
        return "Cop {0}".format(self.color)


class Robber(Player):
    def __init__(self, strategy):
        Player.__init__(self, is_cop=False, taxi_cards=4, bus_cards=3, underground_cards=3, strategy=strategy)
        self.double_moves = 2
        self.black_fare_cards = 5

    def use_double_move(self):
        self.double_moves -= 1

    def use_black_fare_card(self):
        self.black_fare_cards -= 1

    def has_black_fare_card(self):
        return self.black_fare_cards > 0

    def has_double_move(self):
        return self.double_moves > 0

    def get_reward_from_terminal_state(self, terminal_state):
        if terminal_state.robber_won():
            return 1
        else:
            return 0

    def should_use_blackfare_card(self, round, actions, uses_move_filtering):
        if uses_move_filtering:
            return self.has_black_fare_card() and MoveFiltering.should_use_blackfare_optimal(round, actions)
        else:
            return self.has_black_fare_card() and MoveFiltering.should_use_blackfare_greedy()

    def should_use_double_move(self, players, uses_move_filtering):
        if uses_move_filtering:
            return self.has_double_move() and MoveFiltering.should_use_double_move_optimal(players)
        else:
            return self.has_double_move() and MoveFiltering.should_use_double_move_greedy()

    def __repr__(self):
        return "Robber"


POSSIBLE_POSITIONS = [0, 4, 8, 16]
POSSIBLE_STARTING_POSITIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
DISTANCE_TO_COP = [0.196, 0.671, 0.540, 0.384, 0.196]


class PlayersOnGraph:
    def __init__(self, players):
        self.graph = Graph()
        self.players = PlayersOnGraph.normalize_players_list(players)
        self.current_player = 0
        self.current_positions = self.generate_starting_positions()
        self.robber_possible_locations = filter(lambda l: l not in self.get_cops_positions(),
                                                POSSIBLE_STARTING_POSITIONS)
        self.most_probable_robber_position = random.choice(self.robber_possible_locations)
        self.prev_most_probable_robber_position = None

    @staticmethod
    def normalize_players_list(players):
        if type(players[0]) is not Robber:
            i = [i for i, p in enumerate(players) if isinstance(p, Robber)][0]
            tmp = players[0]
            players[0] = players[i]
            players[i] = tmp
        for p in players[1:]:
            if isinstance(p, Robber): players.remove(p)
        return players if len(players) <= 6 else players[:6]

    def generate_starting_positions(self):
        positions = set()
        for player in self.players:
            pos = random.choice(POSSIBLE_STARTING_POSITIONS)
            while pos in positions:
                pos = random.choice(POSSIBLE_STARTING_POSITIONS)
            positions.add(pos)
            player.position = pos
        return list(positions)

    def get_cops_positions(self):
        return self.current_positions[1:]

    def get_robber_position(self):
        return self.current_positions[0]

    def get_avg_distance_from_robber(self):
        robber = self.get_robber_position()
        dist = map(lambda cop: self.graph.get_shortest_distance_between_points(robber, cop), self.get_cops_positions())
        return int(sum(dist) / len(dist))

    def get_player_at_index(self, i):
        return self.players[i]

    def is_player_cop(self, i):
        return self.players[i].is_cop

    def is_player_robber(self, i):
        return not self.players[i].is_cop

    def cop_definitely_caught_robber(self, cop):
        return cop.position() == self.get_robber_position()

    def cops_definitely_caught_robber(self):
        for cop in self.get_cops_positions():
            if cop == self.get_robber_position(): return True
        return False

    def cop_most_probably_caught_robber(self, cop):
        return cop.position() in self.robber_possible_locations

    def cops_most_probably_caught_robber(self):
        for cop in self.get_cops_positions():
            if cop in self.robber_possible_locations: return True
        return False

    def shortest_distance_between_pos_and_cop(self, pos):
        return min(map(lambda cop: self.graph.get_shortest_distance_between_points(pos, cop, is_cop=False),
                       self.get_cops_positions()))

    def shortest_distance_between_robber_and_pos(self, pos):
        return self.graph.get_shortest_distance_between_points(self.most_probable_robber_position, pos, is_cop=True)

    def get_most_probable_robber_position(self):
        if not self.robber_possible_locations: return -1
        cops = self.get_cops_positions()
        probs = [0.0] * len(self.robber_possible_locations)
        for i in xrange(len(self.robber_possible_locations)):
            loc = self.robber_possible_locations[i]
            min_dist = min(
                map(lambda cop: self.graph.get_shortest_distance_between_points(loc, cop, is_cop=False), cops))
            p_i = min_dist - 1 if min_dist < 6 else 4
            probs[i] = DISTANCE_TO_COP[p_i]
        true = True
        chosen = 0
        max_p = max(probs)
        while true:
            chosen = random.randint(0, 4)
            if random.random() < probs[chosen] / max_p:
                true = False
        return self.robber_possible_locations[chosen]

    def get_actions_for_position(self, pos):
        return self.graph.get_actions_for_position(pos)

    def refresh_robbers_possible_locations(self, transport):
        new_locations = []
        for loc in self.robber_possible_locations:
            if transport == 'black-fare' or transport == Transport.BLACK_FARE:
                new_locations.extend(self.graph.get_destinations_for_position(loc))
            else:
                new_locations.extend(self.graph.get_actions_for_position_by_transport(loc, transport))
            return filter(lambda l: l not in self.get_cops_positions(), new_locations)

    def remove_current_cop_from_possible_locations(self, cop):
        self.robber_possible_locations.remove(self.current_positions[cop])
        self.prev_most_probable_robber_position = self.most_probable_robber_position
        self.most_probable_robber_position = self.get_most_probable_robber_position()

    def refresh_robbers_most_probable_position(self, transport):
        self.robber_possible_locations = self.refresh_robbers_possible_locations(transport)
        self.prev_most_probable_robber_position = self.most_probable_robber_position
        self.most_probable_robber_position = self.get_most_probable_robber_position()

    def set_actual_as_most_probable(self):
        self.robber_possible_locations = [self.get_robber_position()]
        self.prev_most_probable_robber_position = self.most_probable_robber_position
        self.most_probable_robber_position = self.get_robber_position()

    def use_card(self, i, action):
        if self.players[i].is_cop:
            self.players[i].use_card(action.transport)
            self.players[0].get_card(action.transport)
        elif action.transport == 'balck-fare' or action.transport == Transport.BLACK_FARE:
            self.players[0].use_black_fare_card()
        else:
            self.players[0].use_card(action.transport)

    def move_player(self, i, action):
        self.use_card(i, action)
        self.current_positions[i] = action.destination

    def move_player_from_cops_pov(self, i, action):
        self.use_card(i, action)
        if self.players[i].is_cop:
            self.current_positions[i] = action.destination
        else:
            self.prev_most_probable_robber_position = self.most_probable_robber_position
            self.most_probable_robber_position = action.destination

    def get_available_actions_for_player(self, i):
        possible_actions = self.graph.get_actions_for_position(self.current_positions[i])
        possible_actions = filter(lambda a: a.destination not in self.current_positions, possible_actions)
        if not self.players[i].can_ride_taxi:
            possible_actions = filter(lambda a: a.transport == Transport.TAXI or a.transport == 'taxi',
                                      possible_actions)
        if not self.players[i].can_ride_bus:
            possible_actions = filter(lambda a: a.transport == Transport.BUS or a.transport == 'bus', possible_actions)
        if not self.players[i].can_ride_taxi:
            possible_actions = filter(lambda a: a.transport == Transport.UNDERGROUND or a.transport == 'underground',
                                      possible_actions)
        if self.players[i].is_cop or not self.players[i].has_black_fare_card():
            possible_actions = filter(lambda a: a.transport == Transport.BLACK_FARE or a.transport == 'black-fare',
                                      possible_actions)
        return possible_actions

    def get_available_actions__from_cop_pov(self, i):
        if self.players[i].is_cop:
            return self.get_available_actions_for_player(i)
        else:
            return self.get_available_actions_for_player(self.most_probable_robber_position)

    def __repr__(self):
        str_rep = ""
        for p in self.players:
            str_rep += "{0}: position {1} [taxi: {2} | bus: {3} | underground: {4}]\n" \
                .format(p, p.position(), p.taxi_crads, p.bus_cards, p.underground_cards)
        return str_rep

    def uses_coalition_reduction_strategy(self, i):
        return  self.get_player_at_index(i).uses_coalition_reduction_strategy()

    def uses_moves_filtering_strategy(self, i):
        return  self.get_player_at_index(i).uses_move_filtering_strategy()