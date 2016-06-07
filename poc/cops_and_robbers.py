import matplotlib.pyplot as plt
import pylab
import json
import operator
import MCTS
from Graph import Graph
from Guy import Cop, Robber
from Strategies import *


json_file = "data/scotland_yard.json"
json_coordinate_file = "data/scotland_yard_coordination.json"

#json_file = "data/graph.json"
#json_coordinate_file = "data/graph_coordination.json"

scotland_yard = True
human_cop = False
human_robber = False
robber_target = 16    

def get_graph_representation_from_json(json_file, scotland_yard = False):
    with open(json_file) as f:
        board = json.loads(f.read())
    graph_representation = {}
    for key in board.keys():
        graph_representation[int(key)] = []
        for destination in board[key]:
            if scotland_yard:
                graph_representation[int(key)].append(int(destination["destination"]))
            else:
                graph_representation[int(key)].append(int(destination))
    return graph_representation

graph_representation = get_graph_representation_from_json(json_file, scotland_yard)


if __name__ == "__main__":
    speed = 0.1
    pylab.ion()

    graph = Graph(graph_representation)

    #print graph.networkx_graph()
    #print graph.graph

    cop1 = Cop(12, "Janusz", graph)
    robber1 = Robber(1, "Miroslaw", graph)
    pylab.show()
    game_on = True
    robbers, cops = graph.plot_graph(json_coordinate_file, robber_target)
    pylab.draw()

    monte = MCTS.MonteCarloTreeSearch(MCTS.Board(cop1, robber1))

    print "ROBBER:"
    robber_strategy = DiarrheaStrategy(robber_target, graph)
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
