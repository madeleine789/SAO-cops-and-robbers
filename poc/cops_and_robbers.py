import random
import networkx as nx
import matplotlib.pyplot as plt
import pylab
import operator
import MCTS
import json

random.seed()
graph_representation = {0: [1, 4], 1: [0, 2, 5], 2: [1, 3, 6], 3: [2, 7],
                        4: [0, 5, 8], 5: [1, 4, 6, 9], 6: [2, 5, 7, 10], 7: [3, 6, 11],
                        8: [4, 9, 12], 9: [5, 8, 10, 13], 10: [6, 9, 11, 14], 11: [7, 10, 15],
                        12: [8, 13, 16], 13: [9, 12, 14], 14: [10, 13, 15], 15: [11, 14],
                        16: [12]}


class Graph:
    def __init__(self, graph):
        self.graph = graph
        self.robbers = []
        self.cops = []
        self.coordinates = []

    def get_coordinates_for_every_position(self):
        with open("./poc/data/board_coordinate.json") as f:
            board = json.loads(f.read())
        coordinates = {}
        for key in board.keys():
            coordinates[key] = board[key]
        return coordinates

    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = []

    def get_adjacent_nodes(self, node):
        return self.graph[node] if self.graph[node] else None

    def add_directed_edge(self, edge):
        source, target = edge
        self.add_node(source)
        self.add_node(target)
        if source == target:
            raise ValueError("Loops are forbidden")
        if target not in self.graph[source]:
            self.graph[source].append(target)

    def add_undirected_edge(self, edge):
        source, target = edge
        self.add_node(source)
        self.add_node(target)
        if source == target:
            raise ValueError("Loops are forbidden")
        if target not in self.graph[source]:
            self.graph[source].append(target)
        if source not in self.graph[target]:
            self.graph[target].append(source)

    def add_robber(self, robber):
        if robber.position in self.graph:
            self.robbers.append(robber)

    def add_cop(self, cop):
        if cop.position in self.graph:
            self.cops.append(cop)

    def print_graph(self):
        for source in self.graph:
            print source, ":",
            for target in self.graph[source]:
                print target,
            for cop in self.cops:
                if cop.position == source:
                    print "C:" + cop.name,
            for robber in self.robbers:
                if robber.position == source:
                    print "B:" + robber.name,
            print

    def human_robber_move(self):
        robber_id = 0
        if len(self.robbers) > 1:
            print "Robbers' positions: "
            for robber_id in range(len(self.robbers)):
                print "Robber " + str(robber_id) + ": " + str(self.robbers[robber_id].position)
            while True:
                robber_id = int(raw_input("Please choose robber to move:"))
                if robber_id < len(self.robbers):
                    break
        robber = self.robbers[robber_id]

        while True:
            new_position = int(raw_input("Now choose new position for robber: "))
            if new_position in self.graph[robber.position]:
                robber.position = new_position
                break
            else:
                print("Please choose again.")


    def human_cop_move(self):
        cop_id = 0
        if len(self.cops) > 1:
            print "Cops' positions: "
            for cop_id in range(len(self.cops)):
                print "Cop " + str(cop_id) + ": " + str(self.cops[cop_id].position)
            while True:
                cop_id = int(raw_input("Please choose cop to move:"))
                if cop_id < len(self.cops): break
        cop = self.cops[cop_id]

        while True:
            new_position = int(raw_input("Now choose new position for cop: "))
            if new_position in self.graph[cop.position]:
                cop.position = new_position
                break
            else:
                print("Please choose again.")

    def plot_graph(self):
        self.coordinates = self.get_coordinates_for_every_position()

        fig = plt.figure()
        ax = fig.add_subplot(111)

        points_x = []
        points_y = []

        for key in range(0, 17):
            points_x.append(self.coordinates[str(key)][0])
            points_y.append(self.coordinates[str(key)][1])

        for start in self.graph:
            for end in self.graph[start]:
                coordinates_from = self.coordinates[str(start)]
                coordinates_to = self.coordinates[str(end)]
                ax.plot((coordinates_from[0], coordinates_to[0]), (coordinates_from[1], coordinates_to[1]), 'k-')
        plt.axis([-1, 5, -1, 5])

        points, = ax.plot(points_x, points_y, 'wo', picker=5)

        robbers_x = []
        robbers_y = []
        cops_x = []
        cops_y = []

        for robber in self.robbers:
            robbers_x.append(self.coordinates[str(robber.position)][0])
            robbers_y.append(self.coordinates[str(robber.position)][1])

        for cop in self.cops:
            cops_x.append(self.coordinates[str(cop.position)][0])
            cops_y.append(self.coordinates[str(cop.position)][1])

        robbers, = ax.plot(robbers_x, robbers_y, 'ro')
        cops, = ax.plot(cops_x, cops_y, 'bo')

        def onpick(event):
            thisline = event.artist
            xdata = thisline.get_xdata()
            ydata = thisline.get_ydata()
            ind = event.ind
            points = tuple(zip(xdata[ind], ydata[ind]))
            # print('onpick points:', points)
            pressed_point = 0
            for key, value in self.coordinates.iteritems():
                if value[0] == points[0][0] and value[1] == points[0][1]:
                    pressed_point = key
            print
            print "This is " + str(pressed_point) + " position."

        fig.canvas.mpl_connect('pick_event', onpick)
        plt.show()

        return robbers, cops

    def update(self, robbers, cops):
        robbers_x = []
        robbers_y = []
        cops_x = []
        cops_y = []
        for robber in self.robbers:
            robbers_x.append(self.coordinates[str(robber.position)][0])
            robbers_y.append(self.coordinates[str(robber.position)][1])
        for cop in self.cops:
            cops_x.append(self.coordinates[str(cop.position)][0])
            cops_y.append(self.coordinates[str(cop.position)][1])

        robbers.set_xdata(robbers_x)
        robbers.set_ydata(robbers_y)

        cops.set_xdata(cops_x)
        cops.set_ydata(cops_y)

        plt.draw()

    # def plot_graph(self):
    #     g = nx.Graph()
    #     cops = []
    #     robbers = []
    #     for source in self.graph:
    #         for target in self.graph[source]:
    #             g.add_edge(source, target)
    #         for cop in self.cops:
    #             if cop.position == source:
    #                 cops.append(source)
    #         for robber in self.robbers:
    #             if robber.position == source:
    #                 robbers.append(source)
    #     position = nx.spectral_layout(g)
    #     empty = [x for x in self.graph if x not in cops and x not in robbers]
    #     nx.draw_networkx_nodes(g, position, nodelist=robbers, node_color="r")
    #     nx.draw_networkx_nodes(g, position, nodelist=cops, node_color="c")
    #     nx.draw_networkx_nodes(g, position, nodelist=empty, node_color="w")
    #     nx.draw_networkx_edges(g, position)
    #     nx.draw_networkx_labels(g, position)

    def networkx_graph(self):
        g = nx.Graph()
        for source in self.graph:
            for target in self.graph[source]:
                if target not in self.cops_places(): g.add_edge(source, target)
        return g

    def clear_networkx_graph(self, nopes):
        g = nx.Graph()
        neighbours = []
        for i in nopes:
            neighbours += self.graph[i]
        nopes += neighbours
        for source in self.graph:
            if not source in nopes:
                for target in self.graph[source]:
                    if not target in nopes:
                        g.add_edge(source, target)
        return g

    def random_walk_on_graph(self, source):
        all_paths = nx.all_pairs_shortest_path(self.networkx_graph())
        target = random.choice(all_paths[source].keys())
        # Random path is at
        return all_paths[source][target]

    def cops_places(self):
        places = []
        for i in self.cops:
            places.append(i.position)
        return places


class Guy:
    def __init__(self, position, name, graph, prev=None):
        self.position = position
        self.name = name
        self.graph = graph
        self.prev_position = prev

    def change_position(self, new_position):
        if new_position in self.graph.graph[self.position]:
            self.prev_position = self.position
            self.position = new_position


class Cop(Guy):
    def __init__(self, position, name, graph):
        Guy.__init__(self, position, name, graph)
        self.graph.add_cop(self)

    def __repr__(self):
        return "Cop " + self.name


class Robber(Guy):
    def __init__(self, position, name, graph):
        Guy.__init__(self, position, name, graph)
        self.graph.add_robber(self)

    def __repr__(self):
        return "Robber " + self.name


class RStrategy:
    def next_move(self, who): raise NotImplementedError


class CStrategy:
    def next_move(self, who, where): raise NotImplementedError


class RRTstrategy(RStrategy):
    def __init__(self, target):
        self.target = target
        print "    - choosen strategy: RRT"

    def next_move(self, who):
        all_paths = nx.all_pairs_shortest_path(who.graph.networkx_graph())
        print who, ":"
        for i in all_paths:
            print str(i) + "##################################################3"
            for j in all_paths[i]:
                print "    " + str(j) + str(all_paths[i][j])


class NaiveStrategy(RStrategy):
    def __init__(self, target, cannottouch):
        self.target = target
        self.cannottouch = cannottouch
        print "    - choosen strategy: Naive"

    def next_move(self, who):
        all_paths = nx.all_pairs_shortest_path(who.graph.clear_networkx_graph(self.cannottouch))
        all_paths2 = nx.all_pairs_shortest_path(who.graph.networkx_graph())
        if who.position in all_paths:
            if self.target in all_paths[who.position]:
                if len(all_paths[who.position][self.target]) > 1:
                    # print "way to target available"
                    return all_paths[who.position][self.target][1]
            else:
                # print "way to target NOT available"
                for i in all_paths[who.position].values():
                    if len(i) > 1: return i[1]
        else:
            if len(all_paths2[who.position][self.target]) == 2:
                return self.target
            temp = []
            for i in graph.graph[who.position]:
                if i in all_paths:
                    temp.append(i)
            if not temp == []:
                if self.target in all_paths2[who.position]:
                    dicti = {}
                    # print
                    for i in temp:
                        # print str(i) + "  " + str(all_paths2[i][self.target])
                        dicti[i] = len(all_paths2[i][self.target])
                    if not dicti == {}:
                        return min(dicti, key=dicti.get)
                    else:
                        return []

                else:
                    # print "way to target NOT available"
                    for i in all_paths[who.position].values():
                        if len(i) > 1: return i[1]
            print "temp: " + str(temp)
            if self.target in all_paths2[who.position]:
                if len(all_paths2[who.position][self.target]) > 1:
                    print "random way to target available"
                    nextep = all_paths2[who.position][self.target][1]
            else:
                print "random way to target NOT available"
                for i in all_paths2[who.position].values():
                    if len(i) > 1: return i[1]


class MonteStrategy(CStrategy):
    def __init__(self, monte, cop, robber):
        print "    - choosen strategy: MonteStrategy"
        self.monte = monte
        self.cop = cop
        self.robber = robber

    def next_move(self, who=None, where=None):
        import copy
        self.monte.update(MCTS.State(copy.deepcopy(self.cop), copy.deepcopy(self.robber)))
        m = self.monte.next_best_move()
        # print "----------------------- Montec: " + str(m)
        return m


class NaiveCopStrategy(CStrategy):
    def __init__(self):
        print "    - choosen strategy: NaiveCop"

    def next_move(self, who, where):
        all_paths = nx.all_pairs_shortest_path(who.graph.networkx_graph())
        if len(all_paths[who.position][where]) == 2:
            return where
        where = who.graph.graph[where]
        targets = {}
        for w in where:
            targets[w] = len(all_paths[who.position][w])
        targets = sorted(targets.items(), key=operator.itemgetter(1))
        for i in targets:
            if i[1] > 1:
                where = i[0]
                break

        if who.position in all_paths:
            if where in all_paths[who.position]:
                if len(all_paths[who.position][where]) > 1: return all_paths[who.position][where][1]
            else:
                for i in all_paths[who.position].values():
                    if len(i) > 1: return i[1]
        else:
            tmp = random.choice(all_paths2[who.position])
            while len(tmp) < 2: tmp = random.choice(all_paths2[who.position])
            return tmp[1]


class SimpleStrategy(CStrategy):
    def __init__(self):
        print "    - choosen strategy: simple"

    def next_move(self, who):
        print ""


if __name__ == "__main__":
    speed = 0.5
    pylab.ion()
    graph = Graph(graph_representation)

    print graph.networkx_graph()
    print graph.graph

    cop1 = Cop(12, "Janusz", graph)
    robber1 = Robber(1, "Miroslaw", graph)
    pylab.show()
    game_on = True
    graph.plot_graph()
    pylab.draw()

    monte = MCTS.MonteCarloTreeSearch(MCTS.Board(cop1, robber1))

    print "ROBBER:"
    robber_strategy = NaiveStrategy(16, graph.cops_places())
    # robber_strategy = MonteStrategy(16, monte)
    print "COP:"
    # cop_strategy = NaiveCopStrategy()
    cop_strategy = MonteStrategy(monte, cop1, robber1)

    while game_on:
        rp_cop = graph.random_walk_on_graph(cop1.position)
        rp_robber = graph.random_walk_on_graph(robber1.position)

        robber_strategy.cannottouch = graph.cops_places()
        plt.pause(speed)
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
        robber1.change_position(robber_strategy.next_move(robber1))
        graph.plot_graph()
        pylab.draw()
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
        cop1.change_position(cop_strategy.next_move(cop1, robber1.position))
        graph.plot_graph()
        pylab.draw()
