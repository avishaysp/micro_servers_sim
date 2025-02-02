import simpy
import random

from tasks.task import Task


class LoadBalancer:

    def __init__(self, micro_services, method, env, task_list):
        self.micro_services = micro_services
        self.method = method  #round-robin(rr), random(rand), or least-loaded(ll)
        self.index_for_rr = 0
        self.env = env
        self.queue = simpy.Store(env)
        self.task_list = task_list

    def send_packet(self):
        while True:
            if self.queue.items:  # Check if there are items in the queue
                packet = yield self.queue.get()
                print(f"{self.env.now}: packet {packet.id} arrived")
                if self.method == "rr":
                    self.env.process(self._send_packet_rr(packet))
                elif self.method == "rand":
                    self.env.process(self._send_packet_rand(packet))
                else:
                    self.env.process(self._send_packet_ll(packet))
                continue
            else:
                yield self.env.timeout(0.01)

    def _send_packet_rr(self, packet):
        for subtask in packet.subtasks:
            self._update_task_list_start_time(subtask)
            yield self.micro_services[self.index_for_rr].queue.put(subtask)
            self.index_for_rr = (self.index_for_rr + 1) % len(self.micro_services)

    def _send_packet_rand(self, packet):
        for subtask in packet.subtasks:
            self._update_task_list_start_time(subtask)
            micro_service_idx = random.randint(0, len(self.micro_services) - 1)
            yield self.micro_services[micro_service_idx].queue.put(subtask)

    def _send_packet_ll(self, packet):
        for subtask in packet.subtasks:
            self._update_task_list_start_time(subtask)
            min_subtasks_in_queue = len(self.micro_services[0].queue.items)
            min_micro_service = self.micro_services[0]
            for micro_service in self.micro_services:
                if len(micro_service.queue.items) < min_subtasks_in_queue:
                    min_subtasks_in_queue = len(micro_service.queue.items)
                    min_micro_service = micro_service

            yield min_micro_service.queue.put(subtask)

    def _update_task_list_start_time(self, subtask):
        if not self.task_list.tasks_list[subtask.parent_task]:
            self.task_list.tasks_list[subtask.parent_task] = Task(subtask.parent_task, self.env.now)
