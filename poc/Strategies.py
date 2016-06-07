import networkx as nx
import MCTS

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
    def __init__(self, target, graph):
        self.target = target
        self.graph = graph
        self.cannottouch = graph.cops_places()
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
            for i in self.graph.graph[who.position]:
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