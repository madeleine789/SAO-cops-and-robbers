from aenum import Enum


class Transport(Enum):
    TAXI, BUS, UNDERGROUND, BLACK_FARE = range(4)


class Action:
    def __init__(self, destination, transport):
        self.destination = destination
        self.transport = transport

    def __repr__(self):
        return "to {0} by {1}".format(self.destination, self.transport)

    def __eq__(self, other):
        if other != type(Action): return False
        else: return other.destination == self.destination and other.transport == self.transport
