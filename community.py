import random as rd
import networkx as nx
import numpy as np
from statsmodels.stats.proportion import proportion_confint

import random
from collections import Counter


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
        # Todo: add assertion like:
        # assert number_of_elites < number_of_nodes
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
        self.edges = edges

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
            self.initialize_neighborhood()
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
        self.initialize_neighborhood()
        return self.network

    def initialize_neighborhood(self):
        self.neighborhood = dict()
        for node in self.nodes:
            self.neighborhood[node] = list(self.network[node]) + [node]

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

    def total_influence_elites(self):
        edges_to_elites = [
            (source, target)
            for (source, target) in self.network.edges()
            if target in self.nodes_elite
        ]
        return len(edges_to_elites)

    def total_influence_mass(self):
        return len(self.network.edges()) - self.total_influence_elites()

    # TODO (hein)
    # 1. Estimated accuracy seems very inaccurate. Perhaps do binomial proportion
    #  confidence interval? 2. Perhaps move this function outside the class?
    def estimated_community_accuracy(
        self, number_of_voting_simulations, alpha: float = 0.05
    ):
        vote_outcomes = [self.vote() for _ in range(number_of_voting_simulations)]
        number_of_success = len(
            [outcome for outcome in vote_outcomes if outcome == "mass"]
        )
        estimated_accuracy = number_of_success / number_of_voting_simulations
        confidence_interval = proportion_confint(
            number_of_success, number_of_voting_simulations, alpha=alpha
        )
        result = {
            "accuracy": estimated_accuracy,
            "precision": max(confidence_interval) - min(confidence_interval),
        }
        return result

    def vote(self):
        elite_opinion_influence_counter = self.count_elite_influence()
        
        elite_votes = 0
        for node in elite_opinion_influence_counter:
            if elite_opinion_influence_counter[node] > self.degree / 2:
                elite_votes = elite_votes + 1
            elif elite_opinion_influence_counter[node] == self.degree / 2:
                elite_votes = elite_votes + random.randint(0, 1)

        if elite_votes > self.number_of_nodes / 2:
            return 1
        elif elite_votes == self.number_of_nodes / 2:
            return random.randint(0, 1)
        else:
            return 0

    def count_elite_influence(self):
        nodes_influenced_by_elite_opinion = []
        for node_elite in self.nodes_elite:
            if rd.random() < self.elite_competence:
                nodes_influenced_by_elite_opinion.extend(self.neighborhood[node_elite])

        for node_mass in self.nodes_mass:
            if rd.random() > self.mass_competence:
                nodes_influenced_by_elite_opinion.extend(self.neighborhood[node_mass])

        return Counter(nodes_influenced_by_elite_opinion)
