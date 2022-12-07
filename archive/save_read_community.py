import ast

from community import Community


def save_community_to_file(file: str, community: Community):
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
    file = open(f"{file}.txt", "w")
    file.write(community_str)
    file.close()


def read_community_from_file(file: str):
    file = open(f"{file}.txt", "r")
    community_dict = ast.literal_eval(file.read())  # turns the dictionary string into
    # dictionary object
    community = Community(**community_dict)
    return community
