import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from collections import deque

# Initialization
CAPACITY = 15
TRAVEL_PER_FLOOR = 2


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

    def __init__(self, start_floor):
        self.floor = start_floor
        self.capacity = CAPACITY
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

class Floor:

    def __init__(self, number):
        self.number = number
        self.queues = {1: deque(), -1: deque()}

    def has_call(self, direction):
        return len(self.queues[direction]) > 0

    def add(self, passenger):
        self.queues[passenger.direction].append(passenger)



class Controller:

    def __init__(self, num_floors, num_elevators, arrival_lambdas, destination_dist, sim_seed, end_time):
        self.seed = sim_seed
        self.time = 0
        self.end_time = end_time
        self.floors = [Floor(i) for i in range(num_floors)]
        self.destination_dist = destination_dist
        self.arrival_lambdas = arrival_lambdas

        self.arrivals_by_floor = []
        self.destinations_by_floor = []
        for i in range(num_floors):
            floor_seed = self.seed + 1000 * i
            self.arrivals_by_floor.append(self.generate_arrival(arrival_lambdas[i], end_time, floor_seed))
            floor_destination_seed = self.seed + 1000 * i + 500
            self.destinations_by_floor.append(self.generate_destinations(i, floor_destination_seed))
    

        self.elevator_list = []
        for i in range(num_elevators):
            self.elevator_set.append(Elevator(0))
            



    def generate_arrival(self, lam, end_time, seed):
        rng = np.random.default_rng(seed=seed)
        interarrivals = []
        time = 0
        while True:
            u = 1 - rng.random()                # use 1 - u cuz u can be 0
            interarriv = -(1 / lam) * np.log(u)
            if time + interarriv >= end_time:     # next arrival would be past the cutoff
                break
            time += interarriv
            interarrivals.append(interarriv)
        return interarrivals


    def generate_destinations(self, floor, seed):
        rng = np.random.default_rng(seed=seed)
        destinations = []
        arrival_set = self.arrivals_by_floor[floor]
        scaled_destination_dist = self.rescale_dist(floor, self.destination_dist)
        destinations.append(rng.choice(np.arange(0, len(self.floors)), size=len(arrival_set), p=scaled_destination_dist))
        return destinations

    @staticmethod
    def rescale_dist(floor, prob_dist):
        distribution = prob_dist.copy()
        scaling_factor = 1 - distribution[floor]
        distribution[floor] = 0
        for i in range(len(distribution)):
            distribution[i] = distribution[i] / scaling_factor
        return distribution



