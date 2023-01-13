import config as cfg
from basic_functions import majority_winner

# def test_most_frequent():
#     values = ["a", "b", "c", "a", "b"]
#     assert "a" in most_frequent(values)
#     assert "b" in most_frequent(values)
#     assert len(most_frequent(values)) == 2


def test_majority_winner():
    values = [
        cfg.vote_for_mass,
        cfg.vote_for_elites,
        cfg.vote_for_elites,
        cfg.vote_for_mass,
        cfg.vote_for_elites,
    ]
    assert majority_winner(values) == cfg.vote_for_elites

    values = [
        cfg.vote_for_mass,
        cfg.vote_for_elites,
        cfg.vote_for_elites,
        cfg.vote_for_mass,
    ]
    result = majority_winner(values)
    assert result == cfg.vote_for_elites or result == cfg.vote_for_mass
