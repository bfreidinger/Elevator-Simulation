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


IDLE, MOVING, DWELL = 0, 1, 2

class Elevator:

    def __init__(self, start_floor, capacity):
        self.floor = start_floor
        self.capacity = capacity
        self.direction = 0   # 0 = not moving, 1 = UP, -1 = DOWN
        self.status = IDLE    # 0 = idle, 1 = moving, 2 = loading/unloading
        self.passengers = []
        self.next_floor = None   #the floor the elevator is currently going to

    @property
    def at_capacity(self):
        return len(self.passengers) >= self.capacity

    @property
    def car_calls(self):
        return {p.destination for p in self.passengers}

    def board(self, passenger_queue, time):
        boarded = []
        while passenger_queue and not self.at_capacity:
            next_pass = passenger_queue.popleft()
            next_pass.board_time = time
            self.passengers.append(next_pass)
            boarded.append(next_pass)
        return boarded
    
    
    def depart(self, time):
        departed = [p for p in self.passengers if p.destination == self.floor]
        for d in departed:     
            self.passengers.remove(d)
            d.termination_time = time
        return departed
