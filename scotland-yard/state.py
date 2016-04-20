from players import PlayersOnGraph
from mcts.state import MCTSState

MAX_NUMBER_OF_ROUNDS = 24
HIDER_SURFACES_ROUNDS = [3, 8, 13, 18, 24]
ALL_PLAYERS = 0
ONLY_SEEKERS = 1


class State(MCTSState):
    def __init__(self, graph, players):
        self.players_on_graph = PlayersOnGraph(graph, players)
        self.number_of_players = len(players)
        self.current_round = 1
        self.current_player = 0
        self.previous_player = self.number_of_players - 1
        self.last_mean_of_transport = None
        self.search_is_on = False
        self.cops_are_searching = False

    def get_current_player(self):
        return self.players_on_graph.get_player_at_index(self.current_player)

    def get_prev_player(self):
        return self.players_on_graph.get_player_at_index(self.previous_player)

    def start_search(self):
        self.search_is_on = True
        self.cops_are_searching = self.players_on_graph.is_player_cop(self.current_player)

    def robber_won(self):
        return self.current_round == MAX_NUMBER_OF_ROUNDS

    def cops_won(self):
        if self.search_is_on and self.cops_are_searching:
            return self.players_on_graph.cops_most_probably_caught_robber()
        else:
            return self.players_on_graph.cops_definitely_caught_robber()

    def is_terminal(self):
        return self.cops_won() or self.robber_won()

    def get_available_actions_for_current_player(self):
        pass

    def perform_action_for_current_player(self, action):
        pass

    def skip_current_player(self):
        pass