import simpy

from model.join_fork_model import JoinForkModel
from simulation.stats import save_stats
from simulation.stats_calculator import calculate_avg, calculate_min, calculate_max, calculate_system_utilization, \
    calculate_std
from tasks.task import TaskList
from .test_cases import test_cases_list, percentages, lambdas
from .models import models
from consts import NUMBER_OT_TASKS, FAIL_PROB, TIME_DOWN_LAMBDA, NUMBER_OF_SIM
import numpy as np
import concurrent.futures


def summarize_results(results, model_description):
    save_stats(results, calculate_avg, percentages, "Avg. Processing Time", model_description)
    save_stats(results, calculate_min, percentages, "Min. Processing Time", model_description)
    save_stats(results, calculate_max, percentages, "Max. Processing Time", model_description)
    save_stats(results, calculate_std, percentages, "STD Processing Time", model_description)
    save_stats(results, calculate_system_utilization, percentages, "Utilization Perc", model_description)


def run_model(compute_power, model_to_test, packet_generator, with_fails, network_lambda):
    print(f"###test case running {packet_generator.__name__}")
    env = simpy.Environment()
    task_list = TaskList(NUMBER_OT_TASKS)
    process_time_list = [0 for _ in range(len(model_to_test["mu_list"]))]
    model, adjusted_compute_power = create_model(env, model_to_test, process_time_list, task_list, with_fails, compute_power, network_lambda)
    tasks_generator = packet_generator(adjusted_compute_power, NUMBER_OT_TASKS, env, model)
    env.process(tasks_generator.tasks_generator())
    env.run(until=model.aggregator.stop_event)
    return {"generator": packet_generator.__class__.__name__, "compute_power": adjusted_compute_power,
            "task_results": task_list, "processing_results": process_time_list,
            "mu_list": model_to_test["mu_list"]}


def create_model(env, model_to_test, process_time_list, task_list, with_fails, compute_power, network_lambda):    
    if not with_fails:
        return JoinForkModel(NUMBER_OT_TASKS, env, model_to_test['lb_method'], model_to_test["mu_list"],
                            len(model_to_test["mu_list"]), task_list, process_time_list,
                            network_lambda=network_lambda), compute_power
                            
    adjusted_compute_power = compute_power * (1 + FAIL_PROB*TIME_DOWN_LAMBDA)
    return JoinForkModel(NUMBER_OT_TASKS, env, model_to_test['lb_method'], model_to_test["mu_list"], 
                        len(model_to_test["mu_list"]), task_list, process_time_list, fail_perc=FAIL_PROB,
                        time_down=TIME_DOWN_LAMBDA, network_lambda=network_lambda), adjusted_compute_power


def run_simulation():
    for model in models:
        print(f"###start running model {model['description']}")
        shape = (len(test_cases_list), len(percentages), len(lambdas), NUMBER_OF_SIM)
        results = np.empty(shape, dtype=object)

        with concurrent.futures.ProcessPoolExecutor() as executor:
            future_to_index = {}

            for i, test_case in enumerate(test_cases_list):
                for j, perc in enumerate(percentages):
                    for l, network_lambda in enumerate(lambdas):
                        compute_power = 100 / perc
                        for k in range(NUMBER_OF_SIM):
                            future = executor.submit(run_model, compute_power, model, test_case[0], test_case[1], network_lambda)
                            future_to_index[future] = (i, j, l, k)

            for future in concurrent.futures.as_completed(future_to_index):
                i, j, l, k = future_to_index[future]
                results[i][j][l][k] = future.result()

        # Process results for each lambda separately
        for l, network_lambda in enumerate(lambdas):
            lambda_results = results[:, :, l, :]
            summarize_results(lambda_results, f"{model['description']}_lambda_{network_lambda}")
