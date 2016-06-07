import matplotlib.pyplot as plt
import pylab
import json
import operator
import MCTS
from Graph import Graph
from Guy import Cop, Robber
from Strategies import *


json_file = "data/scotland_yard.json"
json_coordinate_file = "data/scotland_yard_coordinate.json"
human_cop = True
human_robber = True
graph_representation = {0: [1, 4], 1: [0, 2, 5], 2: [1, 3, 6], 3: [2, 7],
                        4: [0, 5, 8], 5: [1, 4, 6, 9], 6: [2, 5, 7, 10], 7: [3, 6, 11],
                        8: [4, 9, 12], 9: [5, 8, 10, 13], 10: [6, 9, 11, 14], 11: [7, 10, 15],
                        12: [8, 13, 16], 13: [9, 12, 14], 14: [10, 13, 15], 15: [11, 14],
                        16: [12]}


def get_graph_representation_from_json(json_file):
    with open(json_file) as f:
        board = json.loads(f.read())
    graph_representation = {}
    for key in board.keys():
        graph_representation[int(key)] = []
        for destination in board[key]:
            graph_representation[int(key)].append(int(destination["destination"]))
    return graph_representation


if __name__ == "__main__":
    speed = 0.5
    pylab.ion()

    graph_representation = get_graph_representation_from_json(json_file)
    graph = Graph(graph_representation)

    #print graph.networkx_graph()
    #print graph.graph

    cop1 = Cop(12, "Janusz", graph)
    robber1 = Robber(1, "Miroslaw", graph)
    pylab.show()
    game_on = True
    robbers, cops = graph.plot_graph(json_coordinate_file)
    pylab.draw()

    monte = MCTS.MonteCarloTreeSearch(MCTS.Board(cop1, robber1))

    print "ROBBER:"
    robber_strategy = NaiveStrategy(16, graph)
    # robber_strategy = MonteStrategy(16, monte)
    print "COP:"
    # cop_strategy = NaiveCopStrategy()
    cop_strategy = MonteStrategy(monte, cop1, robber1)

    while game_on:
        if not human_cop:
            rp_cop = graph.random_walk_on_graph(cop1.position)
        if not human_robber:
            rp_robber = graph.random_walk_on_graph(robber1.position)

        robber_strategy.cannottouch = graph.cops_places()
        if robber1.position == cop1.position:
            game_on = False
            print "after cop move:"
            print "GAME OVER!"
            break
        elif robber1.position == robber_strategy.target:
            game_on = False
            print "after cop move:"
            print "VICTORY!"
            break
        if not human_robber:
            robber1.change_position(robber_strategy.next_move(robber1))
        else:
            graph.human_robber_move()
        pylab.draw()
        graph.update(robbers, cops)
        plt.pause(speed)

        if robber1.position == cop1.position:
            game_on = False
            print "after robber move:"
            print "GAME OVER!"
            break
        elif robber1.position == robber_strategy.target:
            game_on = False
            print "after robber move:"
            print "VICTORY!"
            break

        if not human_cop:
            cop1.change_position(cop_strategy.next_move(cop1, robber1.position))
        else:
            graph.human_cop_move()
        pylab.draw()
        graph.update(robbers, cops)
        plt.pause(speed)
