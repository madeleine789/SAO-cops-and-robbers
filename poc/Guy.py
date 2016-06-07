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