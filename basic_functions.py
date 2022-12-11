import random as rd
from time import time

# Decorator
def time_this_function(func):
    def wrapper(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f"Function {func.__name__!r} executed in {(t2-t1):.6f}s")
        return result

    return wrapper


def majority_winner(values: list):
    total = sum(values)
    threshold_to_win = len(values) / 2
    if total > threshold_to_win:
        return 1
    if total < threshold_to_win:
        return 0
    else:
        return rd.randint(0, 1)
