import json
import os

from community import Community


def edges_compress(edges: list):
    edges = list(edges)
    edges_dict = {}
    for source, target in edges:
        if source not in edges_dict.keys():
            edges_dict[source] = [target]
        else:
            edges_dict[source].append(target)
    return edges_dict


def edges_unpack(edges_dict: dict):
    edges_dict = dict(edges_dict)
    edges = [
        (source, target)
        for source in edges_dict.keys()
        for target in edges_dict[source]
    ]
    return edges


def save_community_to_file(filename: str, community: Community):
    path = os.path.dirname(filename).replace("\\", "/")
    os.makedirs(path, exist_ok=True)
    community_dict: dict = {
        "number_of_nodes": community.number_of_nodes,
        "number_of_elites": community.number_of_elites,
        "degree": community.degree,
        "elite_competence": community.elite_competence,
        "mass_competence": community.mass_competence,
        "probability_preferential_attachment": community.probability_preferential_attachment,
        "probability_homophilic_attachment": community.probability_homophilic_attachment,
        "edges": edges_compress(community.network.edges()),
    }
    with open(f"{filename}", "wb") as f:
        json.dump(community_dict, f, protocol=-1)


def read_community_from_file(filename: str):
    with open(f"{filename}", "rb") as f:
        community_dict = json.load(f)
    edges = edges_unpack(community_dict["edges"])
    community_dict["edges"] = edges
    community = Community(**community_dict)
    return community
