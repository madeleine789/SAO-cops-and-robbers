import random
import datetime, math
import time

human_robber = True
human_cop = True

class Board:

    def __init__(self, graph):
        self.graph = graph

    def start(self):
        # Returns a representation of the starting state of the game.
        player = random.choice(self.graph.cops)
        return State(player, self.graph)

    def current_player(self, state):
        # Takes the game state and returns the current player's
        # number.
        return state.player

    def next_state(self, state, play):
        # Takes the game state, and the move to be applied.
        # Returns the new game state.
        player = next((x for x in state.graph.cops if x.name == state.player), None)
        player = next(x for x in state.graph.robbers if x.name == state.player) if player is None else player

        player.position = play
        state.position = play
        return state

    def legal_plays(self, state_history):
        # Takes a sequence of game states representing the full
        # game history, and returns the full list of moves that
        # are legal plays for the current player.
        state = state_history[-1]
        return state.graph.get_adjacent_nodes(state.position)

    def winner(self, state_history):
        # Takes a sequence of game states representing the full
        # game history.  If the game is now won, return the player
        # number.  If the game is still ongoing, return zero.  If
        # the game is tied, return a different distinct value, e.g. -1.
        state = state_history[-1]
        if self.is_cop(state):
            if state.position == state.graph.robbers[0].position:
                return state.player + 'WON !!!'
        else:
            return 0

    def is_cop(self, state):
        if next((x for x in state.graph.cops if x.name == state.player), None) is not None: return True
        else: return False


class State:
    def __init__(self, player, graph):
        self.position = player.position
        self.graph = graph
        self.player = player.name


class MonteCarloTreeSearch:
    def __init__(self, board, **kwargs):
        # Takes an instance of a Board and optionally some keyword
        # arguments.  Initializes the list of game states and the
        # statistics tables.

        self.max_moves = kwargs.get('max_moves', 100)
        seconds = kwargs.get('time', 2)
        self.C = kwargs.get('C', 1.4)
        self.calculation_time = datetime.timedelta(seconds=seconds)
        self.board = board
        self.states = [board.start()]
        self.wins = {}
        self.plays = {}
        self.max_depth = 0

    def update(self, state):
        # Takes a game state, and appends it to the history.
        self.states.append(state)

    def next_best_move(self):
        # Causes the AI to calculate the best move from the
        # current game state and return it.
        self.max_depth = 0
        state = self.states[-1]
        player = self.board.current_player(state)
        legal = self.board.legal_plays(self.states[:])

        # Bail out early if there is no real choice to be made.
        if not legal:
            return
        if len(legal) == 1:
            return legal[0]
        games = 0
        begin = datetime.datetime.utcnow()
        while datetime.datetime.utcnow() - begin < self.calculation_time:
            self.run_simulation()
            games += 1

        moves_states = [(p, self.board.next_state(state, p)) for p in legal]

        # Display the number of calls of `run_simulation` and the
        # time elapsed.
        print games, datetime.datetime.utcnow() - begin

        # Pick the move with the highest percentage of wins.
        percent_wins, move = max(
            (self.wins.get((player, S), 0) /
             self.plays.get((player, S), 1),
             p)
            for p, S in moves_states
        )

        if percent_wins == 0:
            for p, S in moves_states:
                if S.graph.robbers[0].position in S.graph.get_adjacent_nodes(p):
                    move = p
                else:
                    for pp in S.graph.get_adjacent_nodes(p):
                        if S.graph.robbers[0].position in S.graph.get_adjacent_nodes(pp):
                            move = p

        # Display the stats for each possible play.
        for x in sorted(
                ((100 * self.wins.get((player, S), 0) /
                      self.plays.get((player, S), 1),
                  self.wins.get((player, S), 0),
                  self.plays.get((player, S), 0), p)
                 for p, S in moves_states),
                reverse=True
        ):
            print "{3}: {0:.2f}% ({1} / {2})".format(*x)

        print "Maximum depth searched:", self.max_depth

        return move

    def run_simulation(self):
        # Plays out a "random" game from the current position,
        # then updates the statistics tables with the result.
        plays, wins = self.plays, self.wins
        visited_states = set()
        expand = True
        states_copy = self.states[:]
        state = states_copy[-1]
        player = self.board.current_player(state)

        for t in xrange(1, self.max_moves + 1):
            legal = self.board.legal_plays(states_copy)
            moves_states = [(p, self.board.next_state(state, p)) for p in legal]

            if all(plays.get((player, S)) for p, S in moves_states):
                # If we have stats on all of the legal moves here, use them.
                log_total = math.log(
                    sum(plays[(player, S)] for p, S in moves_states))
                value, move, state = max(
                    ((wins[(player, S)] / plays[(player, S)]) +
                     self.C * math.sqrt(log_total / plays[(player, S)]), p, S)
                    for p, S in moves_states
                )
            else:
                # Otherwise, just make an arbitrary decision.
                move, state = random.choice(moves_states)
            states_copy.append(state)

            # `player` here and below refers to the player
            # who moved into that particular state.
            if expand and (player, state) not in plays:
                expand = False
                plays[(player, state)] = 0
                wins[(player, state)] = 0
                if t > self.max_depth:
                    self.max_depth = t

            visited_states.add((player, state))
            player = self.board.current_player(state)
            winner = self.board.winner(states_copy)
            if winner:
                break

        for player, state in visited_states:
            if (player, state) not in plays:
                continue
            plays[(player, state)] += 1
            if player == winner:
                wins[(player, state)] += 1


def computer_robber_move():
    pass

def computer_human_move():
    pass

if __name__ == '__main__':
    from cops_and_robbers import *

    pylab.ion()
    graph = Graph(graph_representation)    

    cop1 = Cop(10, "Janusz", graph)
    cop2 = Cop(14, "Jerzy", graph)
    robber1 = Robber(5, "Miroslaw", graph)
    board = Board(graph)

    robbers, cops = graph.plot_graph()
    pylab.draw()

    player = "Robber"
    while(True):

        print player + " turn."

        if player == "Robber":
            if human_robber:
                graph.human_robber_move()
            else:
                computer_robber_move()
            player = "Cup"

        elif player == "Cup":
            if human_cop:
                graph.human_cop_move()
            else:
                computer_cop_move()
            player = "Robber"

        graph.update(robbers, cops)


    """
    mcts = MonteCarloTreeSearch(board)
    mcts.next_best_move()
    """

    #plt.pause(0.5)
