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
