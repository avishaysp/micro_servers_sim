import numpy as np
from consts import SHOULD_SAVE
import pandas as pd


from .test_cases import test_case_name


def save_stats(results, func, percentages, func_name, model_description):
    vectorized_func = np.vectorize(func)
    results_after_calc_stat = vectorized_func(results)
    compress_results = np.mean(results_after_calc_stat, axis=2)
    data = {}

    for i, test_case in enumerate(compress_results):
        title = test_case_name[i]
        if SHOULD_SAVE:
            data[title] = test_case

    if SHOULD_SAVE:
        df = pd.DataFrame(data, index=percentages)
        df.to_csv(f"results/{func_name} - {model_description}.csv", index=True)
