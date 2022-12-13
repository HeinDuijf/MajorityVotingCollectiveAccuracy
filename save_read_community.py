import ast
import os

from community import Community


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
        "edges": list(community.network.edges()),
    }
    community_str = str(community_dict)
    with open(filename, "w+") as f:
        f.write(community_str)


def read_community_from_file(filename: str):
    with open(f"{filename}.txt", "r") as f:
        community_dict = ast.literal_eval(
            f.read()
        )  # turns the dictionary string into dictionary object
    community = Community(**community_dict)
    return community
