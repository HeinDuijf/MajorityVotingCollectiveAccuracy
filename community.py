import random as rd

import networkx as nx
import numpy as np
from statsmodels.stats.proportion import proportion_confint

from scripts import config as cfg
from scripts.basic_functions import majority_winner


class Community:
    def __init__(
        self,
        number_of_nodes: int = 100,
        number_of_elites: int = 40,
        degree: int = 6,
        elite_competence: float = 0.7,
        mass_competence: float = 0.6,
        probability_preferential_attachment: float = 0.6,
        probability_homophilic_attachment: float = None,
        edges: list = None,
    ):
        self.number_of_nodes: int = number_of_nodes
        self.number_of_elites: int = number_of_elites
        self.number_of_mass: int = number_of_nodes - number_of_elites
        self.degree: int = degree
        self.elite_competence: float = elite_competence
        self.mass_competence: float = mass_competence
        self.probability_preferential_attachment: float = (
            probability_preferential_attachment
        )
        self.probability_homophilic_attachment: float = (
            probability_homophilic_attachment
        )
        self.edges: list = edges

        self.nodes: list = list(range(number_of_nodes))
        self.nodes_elite: list = self.nodes[: self.number_of_elites]
        self.nodes_mass: list = self.nodes[-self.number_of_mass :]

        # The central method
        self.network = self.create_network()

    def create_network(self):
        """Returns a directed network according to multi-type preferential
        attachment by amending the Barabási-Albert preferential attachment procedure,
        unless edges are given."""
        if self.edges is not None:
            self.network = self.create_network_from_edges()
            self.initialize_node_attributes()
            return self.network

        # Create initial network.
        if self.probability_homophilic_attachment is None:
            # Create network without homophilic influence
            initial_network = (
                self.create_initial_network_without_homophilic_attachment()
            )
        else:
            initial_network = self.create_initial_network_with_homophilic_attachment()

        # Preferential rewiring.
        self.network = self.rewire_network(initial_network)
        self.initialize_node_attributes()
        return self.network

    def create_network_from_edges(self):
        network = nx.DiGraph()
        network.add_nodes_from(self.nodes)
        network.add_edges_from(self.edges)
        return network

    def create_initial_network_without_homophilic_attachment(self):
        # Initialize network and nodes
        initial_network = nx.DiGraph()
        initial_network.add_nodes_from(self.nodes)
        # Add random edges
        for node in self.nodes:
            potential_targets = self.nodes.copy()
            potential_targets.remove(node)
            targets = rd.sample(potential_targets, self.degree)
            edges_from_node = [(node, target) for target in targets]
            initial_network.add_edges_from(edges_from_node)
        return initial_network

    def create_initial_network_with_homophilic_attachment(self):
        # Initialize network and nodes
        initial_network = nx.DiGraph()
        initial_network.add_nodes_from(self.nodes)

        # Homophilic attachment
        for node in self.nodes:
            random_list = np.random.random_sample(self.degree)
            number_targets_same_type = len(
                [x for x in random_list if x < self.probability_homophilic_attachment]
            )
            number_targets_diff_type = self.degree - number_targets_same_type
            if node in self.nodes_elite:
                nodes_same_type = self.nodes_elite.copy()
                nodes_same_type.remove(node)
                nodes_diff_type = self.nodes_mass
            else:
                nodes_same_type = self.nodes_mass.copy()
                nodes_same_type.remove(node)
                nodes_diff_type = self.nodes_elite
            targets_same_type = rd.sample(nodes_same_type, number_targets_same_type)
            targets_diff_type = rd.sample(nodes_diff_type, number_targets_diff_type)
            targets = targets_same_type + targets_diff_type
            edges_from_source = [(node, target) for target in targets]
            initial_network.add_edges_from(edges_from_source)
        return initial_network

    def rewire_network(self, initial_network):
        # Initialize network and nodes
        network = nx.DiGraph()
        network.add_nodes_from(self.nodes)

        # Multi-type preferential attachment
        edges_to_do = list(initial_network.edges()).copy()
        rd.shuffle(edges_to_do)
        for (source, target) in edges_to_do:
            # Define potential targets
            if target in self.nodes_elite:
                nodes_of_target_type = self.nodes_elite
            else:
                nodes_of_target_type = self.nodes_mass
            potential_targets = [
                node
                for node in nodes_of_target_type
                if node not in network[source] and node != source
            ]

            if rd.random() < self.probability_preferential_attachment:
                # Preferential attachment
                list_of_tuples = list(
                    network.in_degree(potential_targets)
                )  # list of tuples of the form (node, in_degree of node)
                potential_targets_in_degrees = list(
                    map(lambda tuple_item: tuple_item[1], list_of_tuples)
                )
                if not potential_targets:
                    break
                elif all(w == 0 for w in potential_targets_in_degrees):
                    # catches the case where all weights are zero
                    target_new = rd.choice(potential_targets)
                else:
                    target_new = rd.choices(
                        population=potential_targets,
                        weights=potential_targets_in_degrees,
                    )[0]
                    # Note on [0]: rd.choices produces a list
            else:
                # Random attachment
                target_new = rd.choice(potential_targets)
            # add edge to new network and remove edge from edges_to_do
            network.add_edge(source, target_new)
        return network

    def initialize_node_attributes(self):
        for elite_node in self.nodes_elite:
            self.network.nodes[elite_node]["type"] = "elite"
            self.network.nodes[elite_node]["competence"] = self.elite_competence
        for mass_node in self.nodes_mass:
            self.network.nodes[mass_node]["type"] = "mass"
            self.network.nodes[mass_node]["competence"] = self.mass_competence

    def total_influence_elites(self):
        edges_to_elites = [
            (source, target)
            for (source, target) in self.network.edges()
            if target in self.nodes_elite
        ]
        return len(edges_to_elites)

    def total_influence_mass(self):
        return len(self.network.edges()) - self.total_influence_elites()

    def voting_simulation(self, number_of_voting_simulations: int, alpha: float = 0.05):
        """ Method for voting simulation.
        :param number_of_voting_simulations
            Number of simulations to estimate the collective accuracy
        :param alpha:
            p-value for confidence interval.
        :returns result: dict
            result["accuracy_vote"]: estimated collective accuracy,
            result["precision_vote"]: the confidence interval associated with p-value
            alpha
            result["mean"
            result["accuracy_pre_influence"]: estimated collective accuracy
            pre influence,
            result["precision_pre_influence"]: the confidence interval associated with
            pre influence
        """
        vote_winners = []
        votes = []
        opinion_winners = []
        opinions = []
        for _ in range(number_of_voting_simulations):
            outcome = self.vote_and_opinion()
            vote_winners.append(outcome["vote_winner"])
            votes.append(outcome["vote"])
            opinion_winners.append(["opinion_winner"])
            opinions.append(outcome["opinion"])

        result_vote_winners = self.calculate_accuracy_and_precision(
            vote_winners, alpha=alpha
        )
        result_opinion_winners = self.calculate_accuracy_and_precision(
            opinion_winners, alpha=alpha
        )
        mean = np.mean(votes)
        median = np.median(votes)
        std = np.std(votes)
        mean_pre_influence = np.mean(opinions)
        median_pre_influence = np.median(opinions)
        std_pre_influence = np.std(opinions)

        result = {
            "accuracy": result_vote_winners["accuracy"],
            "precision": result_vote_winners["precision"],
            "accuracy_pre_influence": result_opinion_winners["accuracy"],
            "precision_pre_influence": result_opinion_winners["precision"],
            "mean": mean,
            "median": median,
            "std": std,
            "mean_pre_influence": mean_pre_influence,
            "median_pre_influence": median_pre_influence,
            "std_pre_influence": std_pre_influence,
        }
        return result

    @staticmethod
    def calculate_accuracy_and_precision(list_of_items, alpha: float = 0.05):
        number_of_items = len(list_of_items)
        number_of_success = len(
            [outcome for outcome in list_of_items if outcome == cfg.vote_for_mass]
        )
        estimated_accuracy = number_of_success / number_of_items
        confidence_interval = proportion_confint(
            number_of_success, number_of_items, alpha=alpha
        )
        result = {
            "accuracy": estimated_accuracy,
            "precision": max(confidence_interval) - min(confidence_interval),
        }
        return result

    def vote_and_opinion(self):
        self.update_votes()
        list_of_opinions = [self.network.nodes[node]["opinion"] for node in self.nodes]
        list_of_votes = [self.network.nodes[node]["vote"] for node in self.nodes]
        output: dict = {
            "vote_winner": majority_winner(list_of_votes),
            "vote": sum([vote == cfg.vote_for_mass for vote in list_of_votes]),
            "opinion_winner": majority_winner(list_of_opinions),
            "opinion": sum(
                [opinion == cfg.vote_for_mass for opinion in list_of_opinions]
            ),
        }
        return output

    def vote(self):
        self.update_votes()
        list_of_votes = [self.network.nodes[node]["vote"] for node in self.nodes]
        return majority_winner(list_of_votes)

    def update_votes(self):
        self.update_opinions()
        for node in self.nodes:
            neighborhood = list(self.network[node]) + [node]
            neighborhood_opinions = [
                self.network.nodes[neighbor_node]["opinion"]
                for neighbor_node in neighborhood
            ]
            self.network.nodes[node]["vote"] = majority_winner(neighborhood_opinions)

    def update_opinions(self):
        for node_elite in self.nodes_elite:
            if rd.random() < self.elite_competence:
                self.network.nodes[node_elite]["opinion"] = cfg.vote_for_elites
            else:
                self.network.nodes[node_elite]["opinion"] = cfg.vote_for_mass
        for node_mass in self.nodes_mass:
            if rd.random() < self.mass_competence:
                self.network.nodes[node_mass]["opinion"] = cfg.vote_for_mass
            else:
                self.network.nodes[node_mass]["opinion"] = cfg.vote_for_elites
