def get_actions_for_every_position():
    return [[]]


def get_distances_for_every_cop():
    return [[]]


def get_distances_for_a_robber():
    return [[]]


class Graph:
    def __init__(self):
        self.actions_for_positions = get_actions_for_every_position()
        self.distances_cops = get_distances_for_every_cop()
        self.distances_robber = get_distances_for_a_robber()

    def get_actions_for_position(self, i):
        return self.actions_for_positions[i]

    def get_destinations_for_position(self, i):
        return map(lambda action: action.destination, self.get_actions_for_position(i))

