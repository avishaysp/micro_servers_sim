models = [
    {"mu_list": [1024], 'lb_method': 'll', 'description': 'model_1'},
    {
        "mu_list": [1 for _ in range(1024)],
        'lb_method': 'rr',
        'description': 'model_2'
    },
    {
        "mu_list": [1 for _ in range(1024)],
        'lb_method': 'll',
        'description': 'model_3'
    },
]
