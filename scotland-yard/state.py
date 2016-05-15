from players import PlayersOnGraph
from mcts.state import MCTSState

MAX_NUMBER_OF_ROUNDS = 24
ROUNDS_WHEN_ROBBER_IS_VISIBLE = [3, 8, 13, 18, 24]
ALL_PLAYERS = 0
ONLY_SEEKERS = 1


class State(MCTSState):
    def __init__(self, players):
        self.players_on_graph = PlayersOnGraph(players)
        self.number_of_players = len(players)
        self.current_round = 1
        self.current_player = 0
        self.previous_player = self.number_of_players - 1
        self.last_transport = None
        self.search_is_on = False
        self.cops_are_searching = True
        self.uses_coalition_reduction = False
        self.uses_move_filtering = False

    def __repr__(self):
        if self.current_round in ROUNDS_WHEN_ROBBER_IS_VISIBLE:
            return "Round {0} with visible robber!".format(self.current_round)
        else:
            return "Round {0}".format(self.current_round)

    def get_current_player(self):
        return self.players_on_graph.get_player_at_index(self.current_player)

    def get_prev_player(self):
        return self.players_on_graph.get_player_at_index(self.previous_player)

    def start_search(self):
        self.search_is_on = True
        self.cops_are_searching = self.players_on_graph.is_player_cop(self.current_player)
        self.uses_move_filtering = self.players_on_graph.uses_moves_filtering_strategy(self.current_player)
        self.uses_coalition_reduction = self.players_on_graph.uses_coalition_reduction_strategy(self.current_player)

    def stop_search(self):
        self.search_is_on = False

    def robber_won(self):
        return self.current_round == MAX_NUMBER_OF_ROUNDS

    def cops_won(self):
        if self.search_is_on and self.cops_are_searching:
            return self.players_on_graph.cops_most_probably_caught_robber()
        else:
            return self.players_on_graph.cops_definitely_caught_robber()

    def cop_won(self, cop):
        if self.search_is_on and self.cops_are_searching:
            return self.players_on_graph.cop_most_probably_caught_robber(cop)
        else:
            return self.players_on_graph.cop_definitely_caught_robber(cop)

    def is_terminal(self):
        return self.cops_won() or self.robber_won()

    def get_available_actions_for_current_player(self):
        if self.search_is_on and self.cops_are_searching:
            actions = self.players_on_graph.get_available_actions__from_cop_pov(self.current_player)
        else:
            actions = self.players_on_graph.get_available_actions_for_player(self.current_player)

        if self.players_on_graph.is_player_robber(self.current_player):
            pass
            # TODO deal with black fare cards
        return actions

    def perform_action_for_current_player(self, action):
        # if action not in self.get_available_actions_for_current_player():
        #     raise Exception
        if self.search_is_on and self.cops_are_searching:
            self.players_on_graph.move_player_from_cops_pov(self.current_player, action)
        else:
            self.players_on_graph.move_player(self.current_player, action)
        if not self.players_on_graph.players[self.current_player].is_cop:
            self.last_transport = action.transport
            if self.current_round in ROUNDS_WHEN_ROBBER_IS_VISIBLE:
                self.players_on_graph.set_actual_as_most_probable()
            else: self.players_on_graph.refresh_robbers_possible_locations(self.last_transport)
        else:
            self.players_on_graph.remove_current_cop_from_possible_locations(self.current_player)
        if self.players_on_graph.is_player_cop(self.current_player) and self.search_is_on:
            robber = self.get_prev_player()
            if robber.should_use_double_move(self.players_on_graph, self.uses_move_filtering):
                self.current_player += 1
                self.current_round += 1
        return self

    def skip_current_player(self):
        if self.current_player == self.number_of_players - 1:
            self.current_round += 1
        self.previous_player = self.current_player
        self.current_player = (self.current_player + 1) % self.number_of_players
        return self

    def update_positions(self):
        self.players_on_graph.prev_most_probable_robber_position = self.players_on_graph.most_probable_robber_position
