class SubTask:
        def __init__(self, subtask_id, parent_task):
            self.id: int = subtask_id
            self.parent_task: int = parent_task

        def __repr__(self):
            return f"SubTask(id={self.id}, task_id={self.parent_task})"


class Packet:
    def __init__(self, packet_id, subtasks):
        self.id: int = packet_id
        self.subtasks: list = subtasks

    def __repr__(self):
        return f"Packet(id={self.id}, subtasks={self.subtasks[0].parent_task})"

class Task:
    def __init__(self, task_id, start_time):
        self.task_id = task_id
        self.start_time = start_time
        self.end_time = 0

    def __repr__(self):
        return f"Task(id={self.task_id}, start time={self.start_time}, end_time={self.end_time})"


class TaskList:
    def __init__(self, number_of_tasks):
        self.tasks_list = [None for i in range(number_of_tasks)]

    def max_end_time(self):
        return max((task.end_time for task in self.tasks_list), default=0)

