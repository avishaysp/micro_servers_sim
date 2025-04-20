import random
import simpy


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
                continue

            subtask = yield self.queue.get()
            process_start = self.env.now
            # print(f"{process_start}: server #{self.ms_id}# start processing subtask {subtask.id} from task {subtask.parent_task}")
            yield self.env.timeout(random.expovariate(self.exp_mu))
            self.process_time_list[self.ms_id] += (self.env.now - process_start)
            # print(f"{self.env.now}: server #{self.ms_id}# done processing subtask {subtask.id} from task {subtask.parent_task}")
            yield self.aggregator.queue.put(subtask)
