import networkx as nx
import matplotlib.pyplot as plt
graph_representation = {0: [1, 4], 1: [0, 2, 5], 2: [1, 3, 6], 3: [2, 7],
                        4: [0, 5, 8], 5: [1, 4, 6, 9], 6: [2, 5, 7, 10], 7: [3, 6, 11],
                        8: [4, 9, 12], 9: [5, 8, 10, 13], 10: [6, 9, 11, 14], 11: [7, 10, 15],
                        12: [8, 13], 13: [9, 12, 14], 14: [10, 13, 15], 15: [11, 14]}


class Graph:
    def __init__(self, graph):
        self.graph = graph
        self.robbers = []
        self.cops = []

    def add_node(self, node):
        if node not in graph:
            graph[node] = []

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

    def plot_graph(self):
        g = nx.Graph()
        cops = []
        robbers = []
        for source in self.graph:
            for target in self.graph[source]:
                g.add_edge(source, target)
            for cop in self.cops:
                if cop.position == source:
                    cops.append(source)
            for robber in self.robbers:
                if robber.position == source:
                    robbers.append(source)
        position = nx.spectral_layout(g)
        empty = [x for x in self.graph if x not in cops and x not in robbers]
        nx.draw_networkx_nodes(g, position, nodelist=cops, node_color="b")
        nx.draw_networkx_nodes(g, position, nodelist=robbers, node_color="r")
        nx.draw_networkx_nodes(g, position, nodelist=empty, node_color="k")
        nx.draw_networkx_edges(g, position)
        plt.show()


class Guy:
    def __init__(self, position, name, graph):
        self.position = position
        self.name = name
        self.graph = graph

    def change_position(self, new_position):
        if new_position in self.graph.graph[self.position]:
            self.position = new_position

    def make_random_move(self):
        pass


class Cop(Guy):
    def __init__(self, position, name, graph):
        Guy.__init__(self, position, name, graph)
        self.graph.add_cop(self)


class Robber(Guy):
    def __init__(self, position, name, graph):
        Guy.__init__(self, position, name, graph)
        self.graph.add_robber(self)


if __name__ == "__main__":
    graph = Graph(graph_representation)

    cop1 = Cop(3, "Janusz", graph)
    bandit1 = Robber(5, "Miroslaw", graph)

    graph.plot_graph()

    bandit1.change_position(6)

    graph.plot_graph()

    cop1.change_position(2)

    graph.plot_graph()


