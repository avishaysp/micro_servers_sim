import simpy
from consts import TASK_SIZE


class Aggregator:
    def __init__(self, number_of_tasks, env, task_list):
        self.number_of_tasks = number_of_tasks
        self.env = env
        self.queue = simpy.Store(env)
        self.task_completed = 0
        self.task_status = {i: 0 for i in range(number_of_tasks)}
        self.task_list = task_list

    def aggregate_tasks(self):
        while True:
            if self.queue.items:
                subtask = yield self.queue.get()
                task = subtask.parent_task
                self.task_status[task] += 1
                if self.task_status[task] == TASK_SIZE:
                    print(f"{self.env.now}: task {task} is completed")
                    self.task_completed += 1
                    self.task_list.tasks_list[task].end_time = self.env.now

                if self.task_completed == self.number_of_tasks:
                    print(f"{self.env.now}: All task completed")
            else:
                yield self.env.timeout(0.01)

