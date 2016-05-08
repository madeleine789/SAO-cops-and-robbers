import json
from action import Action
from players import *


def get_actions_for_every_position():
    with open("data/board.json") as f:
        board = json.loads(f.read())
    actions = {}
    for key in board.keys():
        actions[key] = []
        for action in board[key]:
            actions[key].append(Action(action['destination'], action['transport']))
    return actions


def get_distances(file):
    with open(file) as f:
        dist = json.loads(f.read())
    distances = {}
    for key in dist.keys():
        distances[key] = []
        for dest in dist[key]:
            distances[key].append((str(dest['to']), dest['distance']))
    return distances


def get_distances_for_every_cop():
    return get_distances("data/cops.json")


def get_distances_for_a_robber():
    return get_distances("data/robbers.json")


class Graph:
    def __init__(self):
        self.actions_for_positions = get_actions_for_every_position()
        self.distances_cops = get_distances_for_every_cop()
        self.distances_robber = get_distances_for_a_robber()

    def get_actions_for_position(self, i):
        i = i+1
        i = str(i) if type(i) == int else i
        return self.actions_for_positions[i]

    def get_destinations_for_position(self, i):
        i = str(i) if type(i) == int else i
        return map(lambda action: action.destination, self.get_actions_for_position(i))

    def get_shortest_distance_between_points(self, start, end, is_cop=True):
        start = str(start) if type(start) == int else start
        end = str(end) if type(end) == int else end
        if is_cop:
            res = filter(lambda x: x[0] == end, self.distances_cops[start])
        else:
            res = filter(lambda x: x[0] == end, self.distances_robber[start])
        if len(res) > 0:
            return min(res, key=lambda x:x[1])[1]
        elif start == end:
            return 0
        else: return 0

    def get_actions_for_position_by_transport(self, i, transport):
        return filter(lambda x: x.transport == transport, self.get_actions_for_position(i))

    def get_destinations_for_position_by_transport(self, i, transport):
        return map(lambda x: x.destination, self.get_actions_for_position_by_transport(i, transport))

