import random as rd
from itertools import combinations

from statsmodels.stats.proportion import proportion_confint

import scripts.config as cfg

convert_to_text_dict: dict = {
    "p_e": "minority_competence",
    "p_m": "majority_competence",
    "E": "number_of_minority",
    "I_e": "influence_minority_proportion",
    "h": "homophily",
    "c": "competence_selection",
    "dc": "delta_competence",
    "mu": "mean",
    "m": "median",
    "s": "std",
    "v": "vote",
    "a": "accuracy",
    "a-": "accuracy_pre_influence",
}

convert_to_math_dict: dict = {value: key for key, value in convert_to_text_dict.items()}


def majority_winner(values: list):
    """Basic function to determine the majority winner in a binary decision context."""
    number_votes_for_elites = len(
        [value for value in values if value == cfg.vote_for_negative]
    )
    number_votes_for_mass = len(values) - number_votes_for_elites
    threshold = len(values) / 2
    if number_votes_for_elites > threshold:
        return cfg.vote_for_negative
    elif number_votes_for_mass > threshold:
        return cfg.vote_for_positive
    else:
        return rd.choice([cfg.vote_for_positive, cfg.vote_for_negative])


def calculate_accuracy_and_precision(list_of_items, alpha: float = 0.05):
    number_of_items = len(list_of_items)
    number_of_success = len(
        [outcome for outcome in list_of_items if outcome == cfg.vote_for_positive]
    )
    estimated_accuracy = number_of_success / number_of_items
    confidence_interval = proportion_confint(
        number_of_success, number_of_items, alpha=alpha
    )
    result = {
        "accuracy": estimated_accuracy,
        "precision": max(confidence_interval) - min(confidence_interval),
    }
    return result


def convert_math_to_text(math_str: str, output_type: str = "str"):
    """Converts math to text. For example, used to convert "p_e" to
    "minority_competence" and to convert "E + h" to ["number_of_minority","homophily"].
    :param math_str: str
        The string containing math symbols
    :param output_type: str
        Determines the type of the output, either "str" or "list"
    :returns result
        Returns either a string or a list."""
    if output_type == "str":
        result = convert_to_text_dict[math_str]
        return result
    if output_type == "list":
        words = math_str.replace("+", " ").split(" ")
        words = [word for word in words if word != ""]
        result = [
            convert_to_text_dict[word]
            for word in words
            if word in convert_to_text_dict.keys()
        ]
        return result


def convert_text_list_to_math_list(text_list: list):
    result = [convert_to_math_dict[string] for string in text_list]
    return result


def convert_list_to_rows(variables_list: list):
    variables_math_list = [
        convert_to_math_dict[variable] for variable in variables_list
    ]
    items = []
    if "p_m" in variables_math_list and "p_e" in variables_math_list:
        items.append("p_e + p_m")
        variables_math_list.remove("p_m")
        variables_math_list.remove("p_e")
    for value in convert_to_math_dict.values():
        if value in variables_math_list:
            items.append(value)
    rows = items.copy()
    for k in range(2, len(items) + 1):
        subsets_k = list(combinations(items, k))
        for subset_k in subsets_k:
            rows.append(" + ".join(subset_k))
    rows_first = [row for row in rows if "p_m" not in row and "p_e" not in row]
    rows_last = [row for row in rows if "p_m" in row or "p_e" in row]
    rows = rows_first + rows_last
    return rows
