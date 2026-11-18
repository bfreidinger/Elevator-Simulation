import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


class Passenger:

    def __init__(self, id, arrival_time, origin, destination):
        self.id = id
        self.arrival_time = arrival_time
        self.origin = origin
        self.destination = destination
        if origin < destination:
            self.direction = 1
        elif origin > destination:
            self.direction = -1
        else:
            raise Exception(f'origin and destination are the same for passenger {id}')
        self.board_time = None
        self.termination_time = None

    @property
    def wait_time(self):
        return self.board_time - self.arrival_time

    @property
    def total_time(self):
        return self.termination_time - self.arrival_time

