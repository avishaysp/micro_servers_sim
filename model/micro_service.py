import math
import random
import simpy


class MicroService:

    def __init__(self, ms_id, compute_power, env, aggregator, fail_perc, time_down_lambd, process_time_list, network_lambda=1.0):
        self.ms_id = ms_id
        self.compute_power = compute_power
        self.fail_perc = fail_perc
        self.time_down_lambd = time_down_lambd
        self.env = env
        self.queue = simpy.Store(env)
        self.aggregator = aggregator
        self.process_time_list = process_time_list
        self.network_lambda = network_lambda  # Network delay parameter

    def process_subtask(self):
        while True:
            if random.random() < self.fail_perc:
                sigma = 0.5
                yield self.env.timeout(random.lognormvariate(self.time_down_lambd, sigma))

            subtask = yield self.queue.get()
            process_start = self.env.now
            
            # Constant compute time inversely proportional to compute capacity
            compute_time = 1.0 / self.compute_power
            yield self.env.timeout(compute_time)
            
            self.process_time_list[self.ms_id] += (self.env.now - process_start)
            
            # Add exponential networking time before task reaches aggregator
            network_delay = random.expovariate(self.network_lambda)
            yield self.env.timeout(network_delay)
            
            yield self.aggregator.queue.put(subtask)
