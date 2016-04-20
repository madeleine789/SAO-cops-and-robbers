from aetypes import Enum


class Transport(Enum):
    TAXI, BUS, UNDERGROUND = range(3)

class Action:
    def __init__(self, destination, transport):
        self.destination = destination
        self.transport = transport