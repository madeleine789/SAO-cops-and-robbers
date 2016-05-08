from state import State
from mcts.MCTS import MCTreeSearch
from players import *
from strategies import *

MCTS_ITERATIONS = 20000
HIDERS_EXPLORATION = 0.2
SEEKERS_EXPLORATION = 2
MAX_NUMBER_OF_PLAYERS = 6
ROBBERS = 1
COPS = 2
NUMBER_OF_GAMES = 1


def init_players():
    players = [None]*(COPS+1)
    players[0] = Robber([Playouts(used=True), CoalitionReduction(used=True), MoveFiltering(used=True)])
    for i in xrange(1, COPS + 1):
        players[i] = Cop(Color(i-1), strategy=[Playouts(used=True), CoalitionReduction(used=True), MoveFiltering(
            used=True)])
    return players


def init_state(players):
    state = State(players)
    return state


def can_current_player_move(state):
    return len(state.get_available_actions_for_current_player()) > 0


def get_action(state, mcts):
    state.search_is_on = True
    if state.is_terminal():
        state.update_positions()
    expl_param = SEEKERS_EXPLORATION if state.cops_are_searching else HIDERS_EXPLORATION
    action = mcts.perform_search_with_exploration(state, expl_param)
    print action.__repr__
    state.search_is_on = False
    return action


def perform_an_action(state, mcts):
    print state.__repr__()
    print state.get_current_player()
    if can_current_player_move(state):
        action = get_action(state, mcts)
        state.perform_action_for_current_player(action)
    else:
        state.skip_current_player()


def print_result(state):
    pass


def play_a_game(mcts):
    players = init_players()
    state = init_state(players)
    while not state.is_terminal():
        perform_an_action(state, mcts)
    print_result(state)


if __name__ == '__main__':
    mcts = MCTreeSearch(iterations_count=10000)
    for i in xrange(NUMBER_OF_GAMES):
        play_a_game(mcts)