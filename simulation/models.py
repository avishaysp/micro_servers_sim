from consts import TASK_SIZE

models = [
    {
        "mu_list": [TASK_SIZE],
        'lb_method': 'll',
        'description': 'model_1',
    },
    {
        "mu_list": [1 for _ in range(TASK_SIZE)],
        'lb_method': 'rr',
        'description': 'model_2',
    },
    {
        "mu_list": [1 for _ in range(TASK_SIZE)],
        'lb_method': 'll',
        'description': 'model_3',
    },
]
