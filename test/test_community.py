from community import Community
from unittest import mock


def test_degree():
    community = Community(degree=5)
    for node in community.nodes:
        assert community.network.out_degree(node) == 5

    community = Community(degree=10)
    for node in community.nodes:
        assert community.network.out_degree(node) == 10


def test_count_elite_opinion_influence():
    n_nodes = 10
    n_elites = 3
    n_mass = n_nodes - n_elites
    degree = 6
    neighborhood_size = degree + 1

    community = Community(
        degree=degree, number_of_nodes=n_nodes, number_of_elites=n_elites
    )

    # All elites have elite opinion
    with mock.patch("community.random.random", return_value=0):
        nodes_influenced_by_elite_opinion = community.count_elite_opinion_influence()
        assert len(nodes_influenced_by_elite_opinion) == n_elites * neighborhood_size

    # All mass nodes have elite opinion
    with mock.patch("community.random.random", return_value=1):
        nodes_influenced_by_elite_opinion = community.count_elite_opinion_influence()
        assert (
            len(nodes_influenced_by_elite_opinion)
            == (n_nodes - n_elites) * neighborhood_size
        )

    # Only the first node wil have an elite opinion:
    with mock.patch(
        "community.random.random",
        side_effect=[0] + [1] * (n_elites - 1) + [0] * n_mass,
    ):
        nodes_influenced_by_elite_opinion = community.count_elite_opinion_influence()
        assert len(nodes_influenced_by_elite_opinion) == neighborhood_size
        assert nodes_influenced_by_elite_opinion == community.neighborhood[0]


def test_vote():
    n_nodes = 10
    n_elites = 3
    degree = 6

    community = Community(
        degree=degree, number_of_nodes=n_nodes, number_of_elites=n_elites
    )

    # Lot of elite influence:
    with mock.patch.object(
        Community, "count_elite_opinion_influence", return_value=[1, 2, 3, 4, 5, 6] * 4
    ):
        assert community.vote() == 1

    # Too little elite influence:
    with mock.patch.object(
        Community,
        "count_elite_opinion_influence",
        return_value=[1, 2, 3, 4] * 4 + [5] * 2 + [6],
    ):
        assert community.vote() == 0

    # Some ties
    with mock.patch.object(
        Community, "count_elite_opinion_influence", return_value=[1, 2, 3, 4, 5, 6] * 3
    ):
        with mock.patch("community.random.randint", return_value=1):
            assert community.vote() == 1

        with mock.patch("community.random.randint", return_value=0):
            assert community.vote() == 0
