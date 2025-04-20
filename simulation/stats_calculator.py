import numpy as np


def calculate_avg(result):
    list_to_calc = create_args_to_calculate_from_result(result, True)
    return np.average(list_to_calc)


def calculate_min(result):
    list_to_calc = create_args_to_calculate_from_result(result, True)
    return np.min(list_to_calc)


def calculate_max(result):
    list_to_calc = create_args_to_calculate_from_result(result, True)
    return np.max(list_to_calc)


def calculate_std(result):
    list_to_calc = create_args_to_calculate_from_result(result, True)
    return np.std(list_to_calc)


def calculate_system_utilization(result):
    services_utilization_time, mu_list, total_time = create_args_to_calculate_from_result(result, False)
    total_cpu = np.sum(mu_list)
    total_time_cpu = total_time * total_cpu
    return sum(mu_list * services_utilization_time) / total_time_cpu


def create_args_to_calculate_from_result(result, task_time):
    if task_time:
        return np.array([(task.end_time - task.start_time) for task in result["task_results"].tasks_list])
    total_time = result["task_results"].max_end_time()
    return np.array(result["processing_results"]), np.array(result["mu_list"]), total_time
