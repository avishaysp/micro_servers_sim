import simpy

from model.join_fork_model import JoinForkModel
from simulation.graph_plot import create_stat_result_graph
from simulation.stats_calculator import calculate_avg, calculate_min, calculate_max, calculate_system_utilization, \
    calculate_var
from tasks.task import TaskList
from .test_cases import test_cases_list, percentages
from consts import NUMBER_OT_TASKS, FAIL_PROB, TIME_DOWN_LAMBDA, NUMBER_OF_SIM
import numpy as np
import concurrent.futures

test_model = {"mu_list": [1024]}


def summarize_results(results):
    create_stat_result_graph(results, calculate_avg, percentages, "Avg. Processing Time")
    create_stat_result_graph(results, calculate_min, percentages, "Min. Processing Time")
    create_stat_result_graph(results, calculate_max, percentages, "Max. Processing Time")
    create_stat_result_graph(results, calculate_var, percentages, "Var. Processing Time")
    create_stat_result_graph(results, calculate_system_utilization, percentages, "Utilization Perc")


def run_model(lamb, model_to_test, packet_generator, with_fails):
    print(f"###start running model {packet_generator.__name__}")
    env = simpy.Environment()
    task_list = TaskList(NUMBER_OT_TASKS)
    process_time_list = [0 for _ in range(len(model_to_test["mu_list"]))]
    model, new_lamb = create_model(env, model_to_test, process_time_list, task_list, with_fails, lamb)
    tasks_generator = packet_generator(new_lamb, NUMBER_OT_TASKS, env, model)
    env.process(tasks_generator.tasks_generator())
    env.run(until=15000)
    return {"generator": packet_generator.__class__.__name__, "lambda": new_lamb,
            "task_results": task_list, "processing_results": process_time_list,
            "mu_list": model_to_test["mu_list"]}


def create_model(env, model_to_test, process_time_list, task_list, with_fails, lamb):
    if not with_fails:
        return JoinForkModel(NUMBER_OT_TASKS, env, 'll', model_to_test["mu_list"], len(model_to_test["mu_list"]),
                             task_list, process_time_list), lamb
    new_lamb = lamb * (1 + FAIL_PROB*TIME_DOWN_LAMBDA)
    return JoinForkModel(NUMBER_OT_TASKS, env, 'll', model_to_test["mu_list"], len(model_to_test["mu_list"]),
                         task_list, process_time_list, fail_perc=FAIL_PROB, time_down=TIME_DOWN_LAMBDA), new_lamb


def run_simulation():
    shape = (len(test_cases_list), len(percentages), NUMBER_OF_SIM)
    results = np.empty(shape, dtype=object)

    total_runs = len(test_cases_list) * len(percentages) * NUMBER_OF_SIM
    l = 1

    # Use ThreadPoolExecutor for multi-threading
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_index = {}

        for i, test_case in enumerate(test_cases_list):
            for j, perc in enumerate(percentages):
                lamb = 100 / perc
                for k in range(NUMBER_OF_SIM):
                    # print(f"current run: {l} / {total_runs}")
                    future = executor.submit(run_model, lamb, test_model, test_case[0], test_case[1])
                    future_to_index[future] = (i, j, k)
                    l += 1

        # Collect results as threads complete
        for future in concurrent.futures.as_completed(future_to_index):
            i, j, k = future_to_index[future]
            results[i][j][k] = future.result()

    summarize_results(results)
