import random as rd
from itertools import combinations

import scripts.config as cfg

convert_to_text_dict: dict = {
    "p_e": "minority_competence",
    "p_m": "majority_competence",
    "E": "number_of_minority",
    "I_e": "influence_minority_proportion",
    "h": "homophily",
    "mu": "mean",
    "m": "median",
    "s": "std",
}

convert_to_math_dict: dict = {value: key for key, value in convert_to_text_dict.items()}


def majority_winner(values: list):
    """ Basic function to determine the majority winner in a binary decision context."""
    number_votes_for_elites = len(
        [value for value in values if value == cfg.vote_for_elites]
    )
    number_votes_for_mass = len(values) - number_votes_for_elites
    threshold = len(values) / 2
    if number_votes_for_elites > threshold:
        return cfg.vote_for_elites
    elif number_votes_for_mass > threshold:
        return cfg.vote_for_mass
    else:
        return rd.choice([cfg.vote_for_mass, cfg.vote_for_elites])


def convert_math_to_text(string: str):
    """ Converts math to text.
    For example, "p_e" is converted to "minority_competence"."""
    words = string.replace("+", " ").split(" ")
    words = [word for word in words if word != ""]
    if len(words) == 1:
        return convert_to_text_dict[words[0]]
    return [convert_to_text_dict[word] for word in words]


def convert_math_to_list(string: str):
    result = convert_math_to_text(string)
    if type(result) != list:
        result = [result]
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
