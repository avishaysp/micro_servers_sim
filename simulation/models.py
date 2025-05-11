import numpy as np
from consts import TASK_SIZE

models = [
    {
        "mu_list": [TASK_SIZE],
        'lb_method': 'll',
        'description': '1) Monolithic',
    },
    {
        "mu_list": [TASK_SIZE // 2, TASK_SIZE // 2],
        'lb_method': 'll',
        'description': '2) 2 Services',
    },
    {
        "mu_list": [1] + [2 ** i for i in range(int(np.log2(TASK_SIZE)))],
        'lb_method': 'll',
        'description': '3) Logarithmic',
    },
    {
        "mu_list": [1 for _ in range(TASK_SIZE)],
        'lb_method': 'rr',
        'description': '4) Distributed [RR]',
    },
    {
        "mu_list": [1 for _ in range(TASK_SIZE)],
        'lb_method': 'll',
        'description': '5) Distributed [LL]',
    },
]
