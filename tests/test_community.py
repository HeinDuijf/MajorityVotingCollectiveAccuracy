import networkx as nx

from community import Community
from scripts import config as cfg

community_blank = Community(
    0,
    0,
    0,
    0,
    0,
    0,
)
community_without_hom: Community = community_blank
community_with_hom: Community = community_blank
community_from_edges: Community = community_blank
community_with_com: Community = community_blank

params_without_hom: dict = {}
params_with_hom: dict = {}
params_with_com: dict = {}
params_from_edges: dict = {}


def setup_module(module):
    global community_without_hom
    global community_with_hom
    global community_from_edges
    global community_with_com
    global params_without_hom
    global params_with_hom
    global params_from_edges
    global params_with_com

    params_with_com = {
        "number_of_nodes": 100,
        "number_of_elites": 20,
        "degree": 6,
        "elite_competence": 0.8,
        "mass_competence": 0.6,
        "probability_preferential_attachment": 0.6,
        "probability_competence_selection": 0.7,
        "probability_homophilic_attachment": None,
        "edges": None,
    }
    community_with_com = Community(**params_with_com)

    params_without_hom = {
        "number_of_nodes": 100,
        "number_of_elites": 20,
        "degree": 6,
        "elite_competence": 0.8,
        "mass_competence": 0.6,
        "probability_preferential_attachment": 0.6,
        "probability_homophilic_attachment": None,
        "edges": None,
    }
    community_without_hom = Community(**params_without_hom)

    params_with_hom = {
        "number_of_nodes": 200,
        "number_of_elites": 77,
        "degree": 8,
        "elite_competence": 0.5,
        "mass_competence": 0.8,
        "probability_preferential_attachment": 0.6,
        "probability_homophilic_attachment": 0.7,
        "edges": None,
    }
    community_with_hom = Community(**params_with_hom)
    edges = list(nx.complete_graph(30, nx.DiGraph()).edges)
    params_from_edges = {
        "number_of_nodes": 200,
        "number_of_elites": 5,
        "degree": 2,
        "elite_competence": 0.9,
        "mass_competence": 0.6,
        "probability_preferential_attachment": 0.6,
        "probability_homophilic_attachment": 0.7,
        "edges": edges,
    }
    community_from_edges = Community(**params_from_edges)


def check_number_of_nodes(community: Community, params: dict):
    assert community.network.number_of_nodes() == params["number_of_nodes"]
    assert community.number_of_nodes == params["number_of_nodes"]
    assert community.nodes == list(range(params["number_of_nodes"]))


def check_degree(community: Community, params: dict):
    assert all(
        [
            community.network.out_degree[node] == params["degree"]
            for node in community.nodes
        ]
    )


def check_competences(community: Community, params: dict):
    assert community.elite_competence == params["elite_competence"]
    assert community.mass_competence == params["mass_competence"]
    assert all(
        [
            community.network.nodes[node]["competence"] == params["elite_competence"]
            for node in community.nodes_elite
        ]
    )
    assert all(
        [
            community.network.nodes[node]["competence"] == params["mass_competence"]
            for node in community.nodes_mass
        ]
    )


def check_community(community: Community, params: dict):
    check_number_of_nodes(community, params)
    if params["edges"] is None:
        check_degree(community, params)
    check_competences(community, params)


def test_create_initial_network_with_competence_selection():
    global community_with_com
    global params_with_com
    check_number_of_nodes(community_with_com, params_with_com)
    check_degree(community_with_com, params_with_com)


def test_create_initial_network_without_homophilic_attachment():
    global community_without_hom
    global params_without_hom
    check_number_of_nodes(community_without_hom, params_without_hom)
    check_degree(community_without_hom, params_without_hom)


def test_create_initial_network_with_homophilic_attachment():
    global community_with_hom
    global params_with_hom
    check_number_of_nodes(community_with_hom, params_with_hom)
    check_degree(community_with_hom, params_with_hom)


def test_create_network_from_edges():
    global community_from_edges
    global params_from_edges
    check_number_of_nodes(community_from_edges, params_from_edges)
    assert set(params_from_edges["edges"]) == set(community_from_edges.edges)
    assert set(params_from_edges["edges"]) == set(community_from_edges.network.edges())


def test_create_network():
    global community_without_hom
    global params_without_hom
    check_community(community_without_hom, params_without_hom)
    global community_with_hom
    global params_with_hom
    check_community(community_with_hom, params_with_hom)
    global community_from_edges
    global params_from_edges
    check_community(community_from_edges, params_from_edges)


def test_rewire_network():
    nodes_mass = community_without_hom.nodes_mass
    nodes_elite = community_without_hom.nodes_elite
    network_pre = community_without_hom.network
    network_post = community_without_hom.rewire_network(network_pre)
    edges_to_mass_pre = [
        (source, target)
        for (source, target) in network_pre.edges()
        if target in nodes_mass
    ]
    edges_to_mass_post = [
        (source, target)
        for (source, target) in network_post.edges()
        if target in nodes_mass
    ]
    assert len(edges_to_mass_pre) == len(edges_to_mass_post)
    edges_to_elite_pre = [
        (source, target)
        for (source, target) in network_pre.edges()
        if target in nodes_elite
    ]
    edges_to_elite_post = [
        (source, target)
        for (source, target) in network_post.edges()
        if target in nodes_elite
    ]
    assert len(edges_to_elite_pre) == len(edges_to_elite_post)


def test_initialize_node_attributes():
    global community_with_hom
    community_with_hom.initialize_node_attributes()
    nodes_type_elite = [
        node
        for node in community_with_hom.network.nodes()
        if community_with_hom.network.nodes[node]["type"] == "elite"
    ]
    nodes_type_mass = [
        node
        for node in community_with_hom.network.nodes()
        if community_with_hom.network.nodes[node]["type"] == "mass"
    ]
    assert set(community_with_hom.nodes_elite) == set(nodes_type_elite)
    assert set(community_with_hom.nodes_mass) == set(nodes_type_mass)
    elite_competence = community_with_hom.elite_competence
    mass_competence = community_with_hom.mass_competence
    assert all(
        [
            community_with_hom.network.nodes[node]["competence"] == elite_competence
            for node in nodes_type_elite
        ]
    )
    assert all(
        [
            community_with_hom.network.nodes[node]["competence"] == mass_competence
            for node in nodes_type_mass
        ]
    )


def test_total_influence_elites():
    global community_from_edges
    assert community_from_edges.total_influence_elites() == (5 * 29)


def test_total_influence_mass():
    global community_from_edges
    assert community_from_edges.total_influence_mass() == (25 * 29)


def test_update_votes():
    global community_with_hom
    community_with_hom.update_votes()
    for node in community_with_hom.nodes:
        node_vote = community_with_hom.network.nodes[node]["vote"]
        node_has_vote: bool = (
            node_vote == cfg.vote_for_positive or node_vote == cfg.vote_for_negative
        )
        assert node_has_vote


def test_update_opinions():
    global community_with_hom
    community_with_hom.update_opinions()
    for node in community_with_hom.nodes:
        node_opinion = community_with_hom.network.nodes[node]["opinion"]
        node_has_opinion: bool = (
            node_opinion == cfg.vote_for_positive
            or node_opinion == cfg.vote_for_negative
        )
        assert node_has_opinion


def test_estimated_community_accuracy():
    pass


def test_vote():
    pass
