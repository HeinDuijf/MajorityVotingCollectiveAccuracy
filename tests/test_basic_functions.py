from scripts import config as cfg
from scripts.basic_functions import (
    convert_list_to_rows,
    convert_math_to_list,
    convert_math_to_text,
    majority_winner,
)

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


def test_convert_math_to_text():
    assert convert_math_to_text("p_e") == "minority_competence"
    assert convert_math_to_text("p_m") == "majority_competence"
    assert convert_math_to_text("E") == "number_of_minority"
    assert convert_math_to_text("I_e") == "influence_minority_proportion"
    assert convert_math_to_text("h") == "homophily"
    assert convert_math_to_text("p_e + p_m") == [
        "minority_competence",
        "majority_competence",
    ]
    assert convert_math_to_text("p_e + p_m + E") == [
        "minority_competence",
        "majority_competence",
        "number_of_minority",
    ]


def test_convert_math_to_list():
    assert convert_math_to_list("p_e") == ["minority_competence"]
    assert convert_math_to_list("p_m") == ["majority_competence"]
    assert convert_math_to_list("E") == ["number_of_minority"]
    assert convert_math_to_list("I_e") == ["influence_minority_proportion"]
    assert convert_math_to_list("h") == ["homophily"]
    assert convert_math_to_list("p_e + p_m") == [
        "minority_competence",
        "majority_competence",
    ]
    assert convert_math_to_list("p_e + p_m + E") == [
        "minority_competence",
        "majority_competence",
        "number_of_minority",
    ]


def test_convert_list_to_rows():
    variables_list = [
        "minority_competence",
        "majority_competence",
        "number_of_minority",
        "homophily",
    ]
    assert convert_list_to_rows(variables_list) == [
        "E",
        "h",
        "E + h",
        "p_e + p_m",
        "p_e + p_m + E",
        "p_e + p_m + h",
        "p_e + p_m + E + h",
    ]
