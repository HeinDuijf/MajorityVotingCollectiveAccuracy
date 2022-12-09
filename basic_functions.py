import random as rd
from collections import Counter
from time import time


def most_frequent(values: list):
    count = Counter(values)
    max_count = max(count.values())
    return [value for value, count_value in count.items() if count_value == max_count]


def majority_winner(values: list):
    return rd.choice(most_frequent(values))


# Decorator
def time_this_function(func):
    def wrapper(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f"Function {func.__name__!r} executed in {(t2-t1):.4f}s")
        return result

    return wrapper
