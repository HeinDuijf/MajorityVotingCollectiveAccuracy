import random as rd

import config as cfg


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
    string.replace(" ", "")
    string.split("+")
    output = []
    if "p_e" in string:
        output.append("minority_competence")
    if "p_m" in string:
        output.append("majority_competence")
    if "E" in string:
        output.append("number_of_minority")
    if "I_e" in string:
        output.append("influence_minority_proportion")
    if "h" in string:
        output.append("homophily")
    if len(output) == 1:
        output = "".join(output)
    return output
