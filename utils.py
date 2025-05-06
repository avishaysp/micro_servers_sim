import random


def random_array_sum_to_n(n):
    size = random.randint(1, n)
    breakpoints = sorted(random.sample(range(1, n), size - 1))
    array = [b - a for a, b in zip([0] + breakpoints, breakpoints + [n])]
    return array


def weighted_shuffle(lst, weight_factor=0.5):
    shuffled = sorted(lst, key=lambda x: lst.index(x) + random.uniform(-1, 1) * (1 / weight_factor), reverse=False)
    return shuffled
