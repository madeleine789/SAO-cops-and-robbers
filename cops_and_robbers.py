import random
import networkx as nx
import matplotlib.pyplot as plt
import pylab

graph_representation = {0: [1, 4], 1: [0, 2, 5], 2: [1, 3, 6], 3: [2, 7],
                        4: [0, 5, 8], 5: [1, 4, 6, 9], 6: [2, 5, 7, 10], 7: [3, 6, 11],
                        8: [4, 9, 12], 9: [5, 8, 10, 13], 10: [6, 9, 11, 14], 11: [7, 10, 15],
                        12: [8, 13], 13: [9, 12, 14], 14: [10, 13, 15], 15: [11, 14],
                        16: [3]}


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
        nx.draw_networkx_labels(g, position)

    def networkx_graph(self):
        g = nx.Graph()
        for source in self.graph:
            for target in self.graph[source]:
                g.add_edge(source, target)
        return g

    def random_walk_on_graph(self, source):
        all_paths = nx.all_pairs_shortest_path(self.networkx_graph())
        target = random.choice(all_paths[source].keys())
        # Random path is at
        return all_paths[source][target]


class Guy:
    def __init__(self, position, name, graph):
        self.position = position
        self.name = name
        self.graph = graph

    def change_position(self, new_position):
        if new_position in self.graph.graph[self.position]:
            self.position = new_position


class Cop(Guy):
    def __init__(self, position, name, graph):
        Guy.__init__(self, position, name, graph)
        self.graph.add_cop(self)


class Robber(Guy):
    def __init__(self, position, name, graph):
        Guy.__init__(self, position, name, graph)
        self.graph.add_robber(self)

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
        all_paths[who.position]
        if len(all_paths[who.position][self.target]) > 1: return all_paths[who.position][self.target][1]
        
class SimpleStrategy(CStrategy):
    def __init__(self):
        print "    - choosen strategy: simple"
    def next_move(self, who):
        
        print ""
    

if __name__ == "__main__":
    pylab.ion()
    graph = Graph(graph_representation)
    
    print "ROBBER:"
    robber_strategy = RRTstrategy(3)
    print "COP:"
    cop_strategy = RRTstrategy(9)

    cop1 = Cop(10, "Janusz", graph)
    robber1 = Robber(5, "Miroslaw", graph)
    pylab.show()
    game_on = True    
    graph.plot_graph()
    pylab.draw()
    
    while game_on:
        rp_cop = graph.random_walk_on_graph(cop1.position)
        rp_robber = graph.random_walk_on_graph(robber1.position)
        #~ print rp_cop, rp_robber
        
        
        
        plt.pause(1)  
        if robber1.position == cop1.position:
            game_on = False
            print "GAME OVER!"
            break
        elif robber1.position == robber_strategy.target:
            game_on = False
            print "VICTORY!"
            break
        robber1.change_position(robber_strategy.next_move(robber1))
        graph.plot_graph()
        pylab.draw()
        plt.pause(1)
        cop_strategy.target = robber1.position
        if robber1.position == cop1.position:
            game_on = False
            print "GAME OVER!"
            break
        elif robber1.position == robber_strategy.target:
            game_on = False
            print "VICTORY!"
            break
        cop1.change_position(cop_strategy.next_move(cop1))
        graph.plot_graph()
        pylab.draw()
            
            
            
            
            
        #~ for i in xrange(min(len(rp_cop), len(rp_robber))):
            #~ if robber1.position == cop1.position:
                #~ game_on = False
                #~ break
            #~ if i < len(rp_robber):
                #~ if rp_robber[i] != cop1.position:
                    #~ robber1.change_position(rp_robber[i])
            #~ graph.plot_graph()
            #~ pylab.draw()
            #~ plt.pause(0)
            #~ if robber1.position == cop1.position:
                #~ game_on = False
                #~ break
            #~ if i < len(rp_cop):
                #~ cop1.change_position(rp_cop[i])
            #~ graph.plot_graph()
            #~ pylab.draw()
            #~ plt.pause(0)

    


