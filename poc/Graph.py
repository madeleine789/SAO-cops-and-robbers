import networkx as nx
import json
import matplotlib.pyplot as plt
import random

random.seed()

class Graph:
    def __init__(self, graph):
        self.graph = graph
        self.robbers = []
        self.cops = []
        self.coordinates = []

    def get_coordinates_for_every_position(self, json_coordinate_file):
        with open(json_coordinate_file) as f:
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

    def plot_graph(self, json_coordinate_file):
        self.coordinates = self.get_coordinates_for_every_position(json_coordinate_file)
        print "Coordinates:"
        print self.coordinates

        print
        print

        print "Graph:"
        print self.graph

        fig = plt.figure()
        ax = fig.add_subplot(111)

        points_x = []
        points_y = []

        for key in self.coordinates.keys():
            points_x.append(self.coordinates[str(key)][0])
            points_y.append(self.coordinates[str(key)][1])

        for start in self.graph:
            for end in self.graph[start]:
                coordinates_from = self.coordinates[str(start)]
                coordinates_to = self.coordinates[str(end)]
                ax.plot((coordinates_from[0], coordinates_to[0]), (coordinates_from[1], coordinates_to[1]), 'k-')
        #plt.axis([-1, 5, -1, 5])

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