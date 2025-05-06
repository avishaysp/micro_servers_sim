import random
import simpy

from consts import INER_NETWORK_OVERHEAD_FACTOR


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
        self.all_services = None  # Will be set later to access the list of all microservices

    def set_all_services(self, all_services):
        self.all_services = all_services

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
            
            if self.all_services:
                # Scale network delay by the number of other microservices
                num_other_services = len(self.all_services) - 1
                overhead_factor = INER_NETWORK_OVERHEAD_FACTOR ** (num_other_services - 1)
                iner_network_delay = random.expovariate(self.network_lambda) * overhead_factor
            else:
                iner_network_delay = 0.0
            
            network_sending_to_aggregator_delay = random.expovariate(self.network_lambda)
                
            yield self.env.timeout(iner_network_delay + network_sending_to_aggregator_delay)
            
            yield self.aggregator.queue.put(subtask)
