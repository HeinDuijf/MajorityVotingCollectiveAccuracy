import os

from community import Community
from scripts.save_read_community import (
    community_compress,
    community_unpack,
    read_community_from_file,
    save_community_to_file,
)


def test_community_compress():
    params: dict = {
        "number_of_nodes": 100,
        "number_of_elites": 35,
        "degree": 7,
        "elite_competence": 0.75,
        "mass_competence": 0.52,
        "probability_homophilic_attachment": 0.8,
        "probability_preferential_attachment": 0.4,
        "edges": [(0, 1), (0, 2), (1, 2), (1, 9), (3, 10)],
    }
    community = Community(**params)
    community_compressed = community_compress(community)
    assert community_compressed["N"] == params["number_of_nodes"]
    assert community_compressed["E"] == params["number_of_elites"]
    assert community_compressed["d"] == params["degree"]
    assert community_compressed["pe"] == params["elite_competence"]
    assert community_compressed["pm"] == params["mass_competence"]
    assert community_compressed["h"] == params["probability_homophilic_attachment"]
    assert community_compressed["pp"] == params["probability_preferential_attachment"]
    assert community_compressed[0] == "1,2"
    assert community_compressed[1] == "2,9"
    assert community_compressed[3] == "10"


def test_community_unpack():
    community_compressed: dict = {
        "N": 100,
        "E": 35,
        "d": 7,
        "pe": 0.75,
        "pm": 0.52,
        "h": 0.8,
        "pp": 0.4,
        0: "1,2",
        1: "2,9",
        3: "10,2",
    }
    community_unpacked = community_unpack(community_compressed)
    assert community_unpacked.number_of_nodes == community_compressed["N"]
    assert community_unpacked.number_of_elites == community_compressed["E"]
    # assert community_unpacked.degree == params["d"]
    assert community_unpacked.elite_competence == community_compressed["pe"]
    assert community_unpacked.mass_competence == community_compressed["pm"]
    assert (
        community_unpacked.probability_homophilic_attachment
        == community_compressed["h"]
    )
    assert (
        community_unpacked.probability_preferential_attachment
        == community_compressed["pp"]
    )
    for node in community_unpacked.nodes:
        if node in community_compressed.keys():
            assert list(community_unpacked.network[node]) == [
                int(neighbor) for neighbor in community_compressed[node].split(",")
            ]


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
    community_read = read_community_from_file(filename="data/test_community")
    assert community.number_of_nodes == community_read.number_of_nodes
    assert community.number_of_elites == community_read.number_of_elites
    assert community.degree == community_read.degree
    assert community.elite_competence == community_read.elite_competence
    assert community.mass_competence == community_read.mass_competence
    assert (
        community.probability_homophilic_attachment
        == community_read.probability_homophilic_attachment
    )
    assert (
        community.probability_preferential_attachment
        == community_read.probability_preferential_attachment
    )
    community_edges = list(community.network.edges())
    community2_edges = list(community_read.network.edges())
    for edge in community_edges:
        assert edge in community2_edges
    os.remove("data/test_community.pickle")
