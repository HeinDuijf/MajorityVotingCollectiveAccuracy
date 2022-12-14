from community import Community


def test_degree():
    com = Community(degree=5)
    for node in com.nodes:
        assert com.network.out_degree(node) == 5

    com = Community(degree=10)
    for node in com.nodes:
        assert com.network.out_degree(node) == 10
