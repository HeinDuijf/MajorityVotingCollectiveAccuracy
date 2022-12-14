from basic_functions import most_frequent


def test_most_frequent():
    values = ["a", "b", "c", "a", "b"]
    assert "a" in most_frequent(values)
    assert "b" in most_frequent(values)
    assert len(most_frequent(values)) == 2
