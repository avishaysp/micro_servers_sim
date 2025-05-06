import numpy as np
from consts import TASK_SIZE

models = [
    {
        "mu_list": [TASK_SIZE],
        'lb_method': 'll',
        'description': 'Monolithic',
    },
    {
        "mu_list": [TASK_SIZE // 2, TASK_SIZE // 2],
        'lb_method': 'll',
        'description': '2 Services',
    },
    {
        "mu_list": [1] + [2 ** i for i in range(int(np.log2(TASK_SIZE)))],
        'lb_method': 'll',
        'description': 'Logarithmic',
    },
    {
        "mu_list": [1 for _ in range(TASK_SIZE)],
        'lb_method': 'rr',
        'description': 'Distributed (RR)',
    },
    {
        "mu_list": [1 for _ in range(TASK_SIZE)],
        'lb_method': 'll',
        'description': 'Distributed (LL)',
    },
]
