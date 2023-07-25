import random as rd

import scripts.config as cfg


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
    convert: dict = {
        "p_e": "minority_competence",
        "p_m": "majority_competence",
        "E": "number_of_minority",
        "I_e": "influence_minority_proportion",
        "h": "homophily",
    }
    if len(words) == 1:
        return convert[words[0]]
    return [convert[word] for word in words]
