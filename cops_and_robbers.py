graph_representation = {0: [1, 4], 1: [0, 2, 5], 2: [1, 3, 6], 3: [2, 7],
		 4: [0, 5, 8], 5: [1, 4, 6, 9], 6: [2, 5, 7, 10], 7: [3, 6, 11],
		 8: [4, 9, 12], 9: [5, 8, 10, 13], 10: [6, 9, 11, 14], 11: [7, 10, 15],
		 12: [8, 13], 13: [9, 12, 14], 14: [10, 13, 15], 15: [11, 14]}

class Graph:
	def __init__(self, graph):
		self.graph = graph
		self.bandits = []
		self.cups = []

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

	def add_bandit(self, bandit):
		if bandit.position in self.graph:
			self.bandits.append(bandit)

	def add_cup(self, cup):
		if cup.position in self.graph:
			self.cups.append(cup)

	def print_graph(self):
		for source in self.graph:
			print source, ":",
			for target in self.graph[source]:
				print target,
			for cup in self.cups:
				if cup.position == source:
					print "C:" + cup.name,
			for bandit in self.bandits:
				if bandit.position == source:
					print "B:" + bandit.name,		
			print

class Guy:
	def __init__(self, position, name):
		self.position = position
		self.name = name
	def change_position(self, graph, new_position):
		if new_position in graph[self.position]:
			self.position = new_position


class Cup(Guy):
	def __init__(self, position, name):
		Guy.__init__(self, position, name)

class Bandit(Guy):
	def __init__(self, position, name):
		Guy.__init__(self, position, name)

if __name__ == "__main__":
	graph = Graph(graph_representation)
	cup1 = Cup(3, "Janusz")
	graph.add_cup(cup1)

	bandit1 = Bandit(5, "Miroslaw")
	graph.add_bandit(bandit1)

	graph.print_graph()

	bandit1.change_position(graph.graph, 6)

	graph.print_graph()


    	