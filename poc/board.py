import random

from cops_and_robbers import *


class Board:
    def __init__(self, cop, robber, graph_repr=graph_representation):
        self.graph_repr = graph_repr
        self.robber = robber
        self.cop = cop

    def start(self):
        # Returns a representation of the starting state of the game.
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

    def legal_plays(self, state_history, strategy=True):
        # Takes a sequence of game states representing the full
        # game history, and returns the full list of moves that
        # are legal plays for the current player.

        state = state_history[-1]

        legal = filter(lambda x: x != state.player.prev_position, self.graph_repr[state.position]) if len(
            self.graph_repr[state.position]) > 1 else self.graph_repr[state.position]

        if strategy and len(legal) > 1:
            result = []
            for pos in legal:
                if "Robber" in str(state.prev_player) and state.prev_player.position in self.graph_repr[pos]:
                    result.append(pos)
            if len(result) == 0:
                return legal
            else:
                return result
        else:
            return legal

    def winner(self, state_history):
        # Takes a sequence of game states representing the full
        # game history.  If the game is now won, return the player
        # number.  If the game is still ongoing, return zero.  If
        # the game is tied, return a different distinct value, e.g. -1.
        state = state_history[-1]
        if "Cop" in str(state.player) and (state.position == self.robber.position or self.robber.position in self.graph_repr[state.position]):
            # print 'COPS WON !!!'
            return 1, state.player
        else:
            return 0, state.prev_player


class State:
    def __init__(self, player, prev_p=None):
        self.prev_player = prev_p
        self.position = player.position
        self.player = player

    def __repr__(self):
        return "STATE: {0} on node {1}".format(self.player, self.position)
