from community import Community
from save_read_community import (
    edges_compress,
    edges_unpack,
    read_community_from_file,
    save_community_to_file,
)


def test_edges_compress():
    edges = [(0, 1), (0, 2), (1, 2), (1, 9), (3, 10)]
    assert edges_compress(edges) == {0: [1, 2], 1: [2, 9], 3: [10]}


def test_edges_unpack():
    edges_dict = {0: [1, 2], 1: [2, 9], 3: [10]}
    assert edges_unpack(edges_dict) == [(0, 1), (0, 2), (1, 2), (1, 9), (3, 10)]


def test_save_and_read():
    params: dict = {
        "number_of_nodes": 100,
        "number_of_elites": 35,
        "degree": 7,
        "elite_competence": 0.75,
        "mass_competence": 0.52,
        "probability_homophilic_attachment": 0.8,
        "probability_preferential_attachment": 0.4,
    }
    community = Community(**params)
    save_community_to_file(filename="data/test_community", community=community)
    community2 = read_community_from_file(filename="data/test_community")
    assert community.number_of_nodes == community2.number_of_nodes
    assert community.number_of_elites == community2.number_of_elites
    assert community.degree == community2.degree
    assert community.elite_competence == community2.elite_competence
    assert community.mass_competence == community2.mass_competence
    assert (
        community.probability_homophilic_attachment
        == community2.probability_homophilic_attachment
    )
    assert (
        community.probability_preferential_attachment
        == community2.probability_preferential_attachment
    )
    community_edges = list(community.network.edges())
    assert community_edges == community2.edges
