import random

from cops_and_robbers import *


class Board:
    def __init__(self, cop, robber, graph_repr=graph_representation):
        self.graph_repr = graph_repr
        self.robber = robber
        self.cop = cop

    def start(self):
        # Returns a representation of the starting state of the game.
        position = random.choice(self.graph_repr.keys())
        self.cop.position = position
        return State(self.cop, self.robber)

    def current_player(self, state):
        # Takes the game state and returns the current player's
        # number.
        return state.player

    def next_state(self, state, play):
        # Takes the game state, and the move to be applied.
        # Returns the new game state.
        state.player.change_position(play)
        tmp = state.prev_player
        state.prev_player = state.player
        state.player = tmp
        state.position = state.player.position
        return state

    def legal_plays(self, state_history):
        # Takes a sequence of game states representing the full
        # game history, and returns the full list of moves that
        # are legal plays for the current player.
        state = state_history[-1]
        return filter(lambda x: x != state.player.prev_position, self.graph_repr[state.position])

    def winner(self, state_history):
        # Takes a sequence of game states representing the full
        # game history.  If the game is now won, return the player
        # number.  If the game is still ongoing, return zero.  If
        # the game is tied, return a different distinct value, e.g. -1.
        state = state_history[-1]
        if state.position == self.robber.position:
            return state.player.name + ' WON !!!'
        else:
            return 0


class State:
    def __init__(self, player, prev_p=None):
        self.prev_player = prev_p
        self.position = player.position
        self.player = player

    def __repr__(self):
        return "STATE: {0} on node {1}".format(self.player, self.position)


if __name__ == '__main__':
    graph = Graph(graph_representation)
    cop1 = Cop(10, "Janusz", graph)
    robber1 = Robber(5, "Miroslaw", graph)
    board = Board(cop1, robber1)
    legal = board.graph_repr[cop1.position]
    print cop1.position, legal
    state = board.next_state(State(cop1, robber1), random.choice(legal))
    print state.prev_player.prev_position, cop1.position
    states = [state]
    print state.position, board.legal_plays(states)
    state = board.next_state(State(state.player, state.prev_player), random.choice(board.legal_plays(states)))
    states.append(state)
    print state.prev_player, state.player
    state = board.next_state(State(state.player, state.prev_player), random.choice(board.legal_plays(states)))
    states.append(state)
    print state.prev_player, state.player
    print states
