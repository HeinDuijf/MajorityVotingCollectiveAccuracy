import random as rd
from collections import Counter


def most_frequent(values: list):
    count = Counter(values)
    max_count = max(count.values())
    return [value for value, count_value in count.items() if count_value == max_count]


def majority_winner(values: list):
    return rd.choice(most_frequent(values))
