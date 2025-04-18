import random
import simpy
import math


class MicroService:

    def __init__(self, ms_id, exp_lambd, env, aggregator, fail_perc, time_down_lambd, process_time_list):
        self.ms_id = ms_id
        self.exp_mu = exp_lambd
        self.fail_perc = fail_perc
        self.time_down_lambs = time_down_lambd
        self.env = env
        self.queue = simpy.Store(env)
        self.aggregator = aggregator
        self.process_time_list = process_time_list

    def process_subtask(self):
        while True:
            if random.random() < self.fail_perc:
                yield self.env.timeout(random.expovariate(self.time_down_lambs))
            if self.queue.items:
                subtask = yield self.queue.get()
                process_start = self.env.now
                # print(f"{process_start}: server #{self.ms_id}# start processing subtask {subtask.id} from task {subtask.parent_task}")

                # Calculate lognormal parameters
                sigma = 0.5  # Standard deviation for the underlying normal distribution (adjust as needed for shape)
                mean_service_time = 1.0 / self.exp_mu
                # mu = ln(mean) - sigma^2 / 2
                mu = math.log(mean_service_time) - (sigma**2 / 2.0)

                yield self.env.timeout(random.lognormvariate(mu, sigma))

                self.process_time_list[self.ms_id] += (self.env.now - process_start)
                # print(f"{self.env.now}: server #{self.ms_id}# done processing subtask {subtask.id} from task {subtask.parent_task}")
                yield self.aggregator.queue.put(subtask)
            else:
                yield self.env.timeout(0.01)

