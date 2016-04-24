from state import State
from mcts.MCTS import MCTreeSearch
MCTS_ITERATIONS = 20000
HIDERS_EXPLORATION = 0.2
SEEKERS_EXPLORATION = 2
MAX_NUMBER_OF_PLAYERS = 6
ROBBERS = 1
COPS = 2
TEST_PLAYERS = 3


def init_players():
    return []


def init_state(players):
    state = State()
    return state


def perform_an_action():
    pass


def print_result(state):
    pass


def play_a_game():
    players = init_players()
    state = init_state(players)
    while not state.is_terminal:
        perform_an_action()
    print_result(state)


if __name__ == '__main__':
    mcts = MCTreeSearch()
