import simpy
import random
from typing import List, Dict


class ForkJoinTask:
    """Represents a task that can be split into subtasks."""
    def __init__(self, name: str, num_subtasks: int, processing_time_range: (int, int)):
        self.name = name
        self.num_subtasks = num_subtasks
        self.processing_time_range = processing_time_range
        self.subtask_times = [random.randint(*processing_time_range) for _ in range(num_subtasks)]
        
    def __repr__(self):
        return f"ForkJoinTask(name={self.name}, subtasks={self.subtask_times})"


class ForkJoinModel:
    """Base class for a Fork-Join Queue model."""
    def __init__(self, env: simpy.Environment, name: str, result_collector: 'SimulationResult'):
        self.env = env
        self.name = name
        self.results = result_collector
        
    def fork(self, task: ForkJoinTask):
        print(f"{self.env.now}: Forking task '{task.name}' into {task.num_subtasks} subtasks.")
        subtask_durations = task.subtask_times
        return subtask_durations
    
    def join(self, subtask_durations: List[int]):
        max_duration = max(subtask_durations)
        print(f"{self.env.now}: Joining subtasks. Maximum processing time: {max_duration}")
        yield self.env.timeout(max_duration)
        return max_duration
    
    def process_task(self, task: ForkJoinTask):
        start_time = self.env.now
        subtask_durations = self.fork(task)
        max_duration = yield self.env.process(self.join(subtask_durations))
        end_time = self.env.now
        total_time = end_time - start_time
        print(f"{self.env.now}: Task '{task.name}' completed in {total_time} units.")
        self.results.add_result(task.name, {"Total Time": total_time, "Max Subtask Duration": max_duration})
    
    def run(self, tasks: List[ForkJoinTask]):
        for task in tasks:
            self.env.process(self.process_task(task))


class SimulationResult:
    """Stores simulation results and metrics."""
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.results: Dict[str, Dict] = {}
    
    def add_result(self, task_name: str, metrics: Dict):
        self.results[task_name] = metrics
    
    def display(self):
        print(f"\nResults for Model: {self.model_name}")
        for task, metrics in self.results.items():
            print(f"Task: {task}, Metrics: {metrics}")


class SimulationRunner:
    """Runs simulations for different models and test cases."""
    def __init__(self, models: List[type], tasks: List[ForkJoinTask]):
        self.models = models
        self.tasks = tasks
    
    def run_all(self):
        for model_cls in self.models:
            print(f"\nRunning simulation for model: {model_cls.__name__}")
            result_collector = SimulationResult(model_cls.__name__)
            env = simpy.Environment()
            model = model_cls(env, model_cls.__name__, result_collector)
            model.run(self.tasks)
            env.run()
            result_collector.display()


# Dummy Model
class DummyForkJoinModel(ForkJoinModel):
    """A dummy Fork-Join model for testing."""
    def join(self, subtask_durations: List[int]):
        print(f"{self.env.now}: [Dummy] Joining subtasks with simplified processing.")
        # Instead of taking the max duration, wait for a fixed amount of time
        yield self.env.timeout(2)
        print(f"{self.env.now}: [Dummy] Completed joining subtasks.")
        return 2


# Example usage
if __name__ == "__main__":
    # Define sample tasks
    tasks = [
        ForkJoinTask(name="Task1", num_subtasks=3, processing_time_range=(1, 5)),
        ForkJoinTask(name="Task2", num_subtasks=4, processing_time_range=(2, 6)),
    ]

    # List of models to run
    models = [DummyForkJoinModel]

    # Create and run the simulation
    runner = SimulationRunner(models, tasks)
    runner.run_all()
