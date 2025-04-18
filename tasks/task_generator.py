from scipy.stats import poisson
from tasks.task import SubTask, Packet
from utils import random_array_sum_to_n, weighted_shuffle
from consts import TASK_SIZE


class TasksGenerator:
    """Base class for tasks generators"""
    def __init__(self, number_of_tasks, env, model):
        self.number_of_tasks = number_of_tasks
        self.env = env
        self.model = model


class ConstIntervalFixPacketsTask(TasksGenerator):
    """Task with constant interval"""
    def __init__(self, interval, number_of_tasks, env, model):
        super().__init__(number_of_tasks, env, model)
        self.interval = interval

    def tasks_generator(self):
        """Generate task at constant intervals."""
        self.env.process(self.model.run_model())
        for task_id in range(self.number_of_tasks):
            yield self.env.timeout(self.interval)
            subtasks = [SubTask(i, task_id) for i in range(TASK_SIZE)]
            packet = Packet(task_id, subtasks)
            yield self.model.load_balancer.queue.put(packet)


class RandIntervalFixPacketsTask(TasksGenerator):
    def __init__(self, lamdb, number_of_tasks: int, env, model):
        super().__init__(number_of_tasks, env, model)
        self.lamdb = lamdb

    def tasks_generator(self):
        """Generate task at with poisson distribution time intervals."""
        self.env.process(self.model.run_model())
        for task_id in range(self.number_of_tasks):
            yield self.env.timeout(poisson.rvs(self.lamdb))  # Random inter-arrival time
            subtasks = [SubTask(i, task_id) for i in range(TASK_SIZE)]
            packet = Packet(task_id, subtasks)
            yield self.model.load_balancer.queue.put(packet)


class RandIntervalOrderedRandPacketsTask(TasksGenerator):
    def __init__(self, lamdb, number_of_tasks: int, env, model):
        super().__init__(number_of_tasks, env, model)
        self.lamdb = lamdb

    def tasks_generator(self):
        """Generate task at with poisson distribution time intervals."""
        self.env.process(self.model.run_model())
        packet_id = 0
        packets_list = []
        for task_id in range(self.number_of_tasks):
            split_list = random_array_sum_to_n(TASK_SIZE)
            start = 0
            for size in split_list:
                packets_list.append([SubTask(i, task_id) for i in range(start, start + size)])
                start += size

        lambda_scale_factor = self.number_of_tasks / len(packets_list)

        for subtasks in packets_list:
            yield self.env.timeout(poisson.rvs(self.lamdb) * lambda_scale_factor)  # Random inter-arrival time
            packet = Packet(packet_id, subtasks)
            packet_id += 1
            yield self.model.load_balancer.queue.put(packet)


class RandIntervalNotOrderedPacketsTask(TasksGenerator):
    def __init__(self, lamdb, number_of_tasks: int, env, model):
        super().__init__(number_of_tasks, env, model)
        self.lamdb = lamdb

    def tasks_generator(self):
        """Generate task at with poisson distribution time intervals."""
        self.env.process(self.model.run_model())

        packet_id = 0
        packets_list = []
        for task_id in range(self.number_of_tasks):
            split_list = random_array_sum_to_n(TASK_SIZE)
            start = 0
            subtasks_list = []
            for size in split_list:
                subtasks_list.append([SubTask(i, task_id) for i in range(start, start + size)])
                start += size
            for subtasks in subtasks_list:
                packets_list.append(subtasks)

        biased_shaffle = weighted_shuffle(packets_list)
        lambda_scale_factor = self.number_of_tasks / len(packets_list)

        for subtasks_for_packet in biased_shaffle:
            yield self.env.timeout(poisson.rvs(self.lamdb) * lambda_scale_factor)
            packet = Packet(packet_id, subtasks_for_packet)
            packet_id += 1
            yield self.model.load_balancer.queue.put(packet)

