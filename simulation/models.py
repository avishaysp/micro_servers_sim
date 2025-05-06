import numpy as np
from consts import TASK_SIZE

models = [
    {
        "mu_list": [TASK_SIZE],
        'lb_method': 'll',
        'description': 'model_1',
    },
    {
        "mu_list": [TASK_SIZE // 2, TASK_SIZE // 2],
        'lb_method': 'll',
        'description': 'model_2',
    },
    {
        "mu_list": [1 for _ in range(TASK_SIZE)],
        'lb_method': 'rr',
        'description': 'model_3',
    },
    {
        "mu_list": [1 for _ in range(TASK_SIZE)],
        'lb_method': 'll',
        'description': 'model_4',
    },
    {
        "mu_list": [1] + [2 ** i for i in range(int(np.log2(TASK_SIZE)))],
        'lb_method': 'll',
        'description': 'model_5',
    },
]
