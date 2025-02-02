import numpy as np
import matplotlib.pyplot as plt
from consts import SHOULD_SAVE
import pandas as pd


from .test_cases import test_cases_list, percentages


def create_stat_result_graph(results, func, percentages, func_name):
    vectorized_func = np.vectorize(func)
    results_after_calc_stat = vectorized_func(results)
    compress_results = np.mean(results_after_calc_stat, axis=2)
    data = {}

    for i, test_case in enumerate(compress_results):
        title = f"{test_cases_list[i][0].__name__} {'with' if test_cases_list[i][1] else 'without'} drop"
        if SHOULD_SAVE:
            data[title] = test_case
        plt.plot(percentages, test_case, label=f"{title}")
        plt.scatter(percentages, test_case)

    if SHOULD_SAVE:
        df = pd.DataFrame(data, index=percentages)
        df.to_csv(f"results/{func_name}.csv", index=True)
    plt.xlabel("lambdas")
    plt.ylabel(f"{func_name}")
    plt.title(f"{func_name} vs. Lambda")
    plt.legend()

    # Display the plot
    plt.grid(True)
    plt.show()

