import random as rd

from community import Community
from save_read_community import read_community_from_file, save_community_to_file


def generate_communities(
    folder: str,
    number_of_communities: int,
    number_of_nodes: int = 100,
    degree: int = 6,
    probability_preferential_attachment: float = 0.6,
    elite_competence_range=(0.55, 0.95),
    mass_competence_range=(0.55, 0.95),
    number_of_elites_range=(20, 45),
    probability_homophilic_attachment_range=(0.5, 1.0),
):
    for community_number in range(number_of_communities):
        # 0. Randomly initialize variables
        elite_competence: float = rd.uniform(*elite_competence_range)
        mass_competence: float = rd.uniform(*mass_competence_range)
        probability_homophilic_attachment: float = rd.uniform(
            *probability_homophilic_attachment_range
        )
        number_of_elites: int = rd.randint(*number_of_elites_range)

        # 1. Generate community with these parameters
        community = Community(
            number_of_nodes=number_of_nodes,
            number_of_elites=number_of_elites,
            degree=degree,
            elite_competence=elite_competence,
            mass_competence=mass_competence,
            probability_preferential_attachment=probability_preferential_attachment,
            probability_homophilic_attachment=probability_homophilic_attachment,
        )

        # 2. Save network to file
        filename: str = f"{folder}/community{community_number}"
        save_community_to_file(file=filename, community=community)

        # 3. Report progress
        if community_number % (number_of_communities / 100) == 0:
            progress = f"{community_number}%"
            print(f"Progress generate_communities: {progress}")


def process_communities_to_csv(
    folder: str,
    results_file: str,
    number_of_communities: int = 10 ** 5,
    number_of_voting_simulations: int = 10 ** 4,
):
    # 0. Initialize csv file with heading
    head_line = (
        "collective_accuracy,"
        + "collective_accuracy_precision,"
        + "minority_competence, "
        + "majority_competence,"
        + "number_of_minority,"
        + "proportional_influence_minority,"
        + "homophily"
    )
    file = open(results_file, "w")
    file.write(f"{head_line}")
    file.close()

    # 1. For-loop over communities in folder
    for community_number in range(number_of_communities):
        community = read_community_from_file(f"{folder}/community{community_number}")

        result = community.estimated_community_accuracy(number_of_voting_simulations)
        collective_accuracy = result["estimated_accuracy"]
        collective_accuracy_precision = result["precision"]
        minority_competence = community.elite_competence
        majority_competence = community.mass_competence
        number_of_minority = community.number_of_elites
        homophily = community.probability_homophilic_attachment
        total_influence_minority = community.total_influence_elites()
        total_influence_majority = community.total_influence_mass()
        proportional_influence_minority = total_influence_minority / (
            total_influence_minority + total_influence_majority
        )

        # 2. Print results to line in csv file
        data_line = (
            f"{collective_accuracy}, {collective_accuracy_precision}, "
            f"{minority_competence}, {majority_competence}, {number_of_minority}, "
            f"{proportional_influence_minority}, {homophily}"
        )
        file = open(results_file, "a")
        file.write(f"\n{data_line}")
        file.close()

        # 3. Report progress
        if community_number % (number_of_communities / 100) == 0:
            progress = f"{community_number}%"
            print(f"Progress process_communities_to_csv: {progress}")


# def print_results_of_folder_to_file(
#     networks_folder: str, results_location: str, number_of_simulations: int = 100
# ):
#     head_line = (
#         "collective_accuracy"
#         + ","
#         + "vote_satisfaction"
#         + ","
#         + "number_of_edges"
#         + ","
#         + "minority_competence"
#         + ","
#         + "majority_competence"
#         + ","
#         + "number_of_minority"
#         + ","
#         + "number_of_majority"
#         + ","
#         + "total_influence_minority"
#         + ","
#         + "total_influence_majority"
#         + ","
#         + "influence_assortment"
#         + ","
#         + "influence_assortment_majority_average"
#         + ","
#         + "influence_assortment_minority_average"
#         + ","
#         + "vote_median"
#     )
#     file = open(results_location, "a")
#     file.write(str(head_line) + "\n")
#     file.close()
#
#     for network_number in range(1000):
#         network = nx.read_gml(
#             networks_folder + "/network" + str(network_number), destringizer=int
#         )
#
#         vote_data = np.array([], dtype=int)
#         number_of_edges: int = network.number_of_edges()
#         minority_competence = network.nodes[99]["competence"]
#         majority_competence = network.nodes[0]["competence"]
#         number_of_minority = sum(
#             [1 for node in network.nodes() if network.nodes[node]["type"] == "B"]
#         )
#         number_of_majority = 100 - number_of_minority
#
#         """ Get collective accuracy and vote satisfaction and vote data"""
#         collective_accuracy: float = 0
#         vote_satisfaction: float = 0
#         for simulation in range(number_of_simulations):
#             ni.update_opinion(network)
#             ni.update_votes(network)
#             majority_vote = ni.vote_winner(
#                 [network.nodes[node]["vote"] for node in network.nodes()]
#             )
#             vote_outcome: int = sum(
#                 [network.nodes[node]["vote"] for node in network.nodes()]
#             )
#             vote_data = np.append(vote_data, vote_outcome)
#             collective_accuracy = collective_accuracy + majority_vote
#             vote_satisfaction = vote_satisfaction + om.vote_satisfaction_network(
#                 network
#             )
#
#         vote_satisfaction = vote_satisfaction / number_of_simulations
#         collective_accuracy = collective_accuracy / number_of_simulations
#
#         """ Idea to include median (or 25%, 75%, etc) voting outcome in the data in order to estimate vote skew """
#         vote_median = np.median(vote_data)
#
#         """ Get influence degrees """
#         total_influence_minority: float = 0
#         total_influence_majority: float = 0
#         for node in network.nodes():
#             if network.nodes[node]["type"] == "B":
#                 total_influence_minority = total_influence_minority + network.in_degree(
#                     node
#                 )
#             else:
#                 total_influence_majority = total_influence_majority + network.in_degree(
#                     node
#                 )
#         # average_influence_minority = total_influence_minority / number_of_minority
#         # average_influence_majority = total_influence_majority / number_of_majority
#         # group_influence_difference = total_influence_minority - total_influence_majority
#         # individual_influence_difference = average_influence_minority - average_influence_majority
#
#         """ Get influence assortment """
#         ni.update_influence(network)
#         influence_minority = sum(
#             [
#                 network.nodes[node]["influence"]
#                 for node in network.nodes()
#                 if network.nodes[node]["type"] == "B"
#             ]
#         )
#         influence_assortment_minority_average = influence_minority / number_of_minority
#         influence_majority = sum(
#             [
#                 network.nodes[node]["influence"]
#                 for node in network.nodes()
#                 if network.nodes[node]["type"] == "A"
#             ]
#         )
#         influence_assortment_majority_average = influence_majority / number_of_majority
#         influence_assortment = (
#             influence_assortment_minority_average
#             - influence_assortment_majority_average
#         )
#
#         """ Print results to line in csv file """
#         data_line = (
#             str(collective_accuracy)
#             + ","
#             + str(vote_satisfaction)
#             + ","
#             + str(number_of_edges)
#             + ","
#             + str(minority_competence)
#             + ","
#             + str(majority_competence)
#             + ","
#             + str(number_of_minority)
#             + ","
#             + str(number_of_majority)
#             + ","
#             + str(total_influence_minority)
#             + ","
#             + str(total_influence_majority)
#             + ","
#             + str(influence_assortment)
#             + ","
#             + str(influence_assortment_majority_average)
#             + ","
#             + str(influence_assortment_minority_average)
#             + ","
#             + str(vote_median)
#         )
#
#         file = open(results_location, "a")
#         file.write(str(data_line) + "\n")
#         file.close()
#         print(
#             "Results of network "
#             + str(network_number)
#             + " have been printed to a file."
#         )


# print_results_of_folder_to_file(folder='majority_voting/sf_equal',
#                                 results_file='majority_voting/results_equal.csv')
