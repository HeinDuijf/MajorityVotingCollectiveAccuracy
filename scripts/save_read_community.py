import os
import pickle

from community import Community


def community_compress(community: Community):
    edges_dict = {}
    for source, target in community.network.edges():
        if source not in edges_dict.keys():
            edges_dict[source] = f"{target}"
        else:
            edges_dict[source] = f"{edges_dict[source]},{target}"
    community_dict = {
        "N": community.number_of_nodes,
        "E": community.number_of_elites,
        "d": community.degree,
        "pe": community.elite_competence,
        "pm": community.mass_competence,
        "pp": community.probability_preferential_attachment,
        "h": community.probability_homophilic_attachment,
        **edges_dict,
    }
    return community_dict


def combine_community_files(directory_path, output_file):
    result = []
    for d in os.listdir(directory_path):
        if d.endswith(".pickle"):
            with open(os.path.join(directory_path, d), "rb") as f:
                content = pickle.load(f)
            result.append(content)
    with open(output_file, "wb") as out:
        pickle.dump(result, out)


def community_unpack(community_compressed: dict):
    nodes = [
        node
        for node in range(community_compressed["N"])
        if node in community_compressed.keys()
    ]
    edges = [
        (source, int(target))
        for source in nodes
        for target in community_compressed[source].split(",")
    ]
    community_dict = {
        "number_of_nodes": community_compressed["N"],
        "number_of_elites": community_compressed["E"],
        "degree": community_compressed["d"],
        "elite_competence": community_compressed["pe"],
        "mass_competence": community_compressed["pm"],
        "probability_preferential_attachment": community_compressed["pp"],
        "probability_homophilic_attachment": community_compressed["h"],
        "edges": edges,
    }
    community = Community(**community_dict)
    return community


def save_community_to_file(filename: str, community: Community):
    path = os.path.dirname(filename).replace("\\", "/")
    os.makedirs(path, exist_ok=True)
    community_compressed = community_compress(community)
    with open(f"{filename}.pickle", "wb") as f:
        pickle.dump(community_compressed, f)


def read_community_from_file(filename: str):
    with open(f"{filename}.pickle", "rb") as f:
        community_compressed = pickle.load(f)
    community = community_unpack(community_compressed)
    return community


def read_community_from_combined_file(filename: str, community_number: int):
    if not filename.endswith(".pickle"):
        filename += ".pickle"
    with open(f"{filename}", "rb") as f:
        community_compressed = pickle.load(f)[community_number]
    community = community_unpack(community_compressed)
    return community
