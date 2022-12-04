import random as rd

import networkx as nx
from statsmodels.stats.proportion import proportion_confint

from basic_functions import majority_winner


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
    ):
        self.number_of_nodes: int = number_of_nodes
        self.number_of_elites: int = number_of_elites
        self.number_of_mass: int = number_of_nodes - number_of_elites
        self.degree: int = degree
        self.elite_competence: float = elite_competence
        self.mass_competence: float = mass_competence
        self.probability_preferential_attachment: float = probability_preferential_attachment
        self.probability_homophilic_attachment: float = probability_homophilic_attachment

        self.nodes: list = list(range(number_of_nodes))
        self.nodes_elite: list = self.nodes[: self.number_of_elites]
        self.nodes_mass: list = self.nodes[-self.number_of_mass :]
        self.network = self.create_network()

        # To keep the computational complexity to a minimum, the following variables
        # are not initialized

    def create_network(self):
        """Returns a directed network according to multi-type preferential
        attachment by amending the Barabási–Albert preferential attachment procedure."""
        # Create initial network
        if self.probability_homophilic_attachment is None:
            # Create network without homophilic influence
            initial_network = (
                self.create_initial_network_without_homophilic_attachment()
            )
        else:
            initial_network = self.create_initial_network_with_homophilic_attachment()

        # Preferential rewiring
        self.network = self.rewire_network_using_preferential_attachment(
            initial_network
        )
        self.initialize_node_attributes()
        return self.network

    def create_initial_network_without_homophilic_attachment(self):
        number_of_edges = self.number_of_nodes * self.degree
        initial_network = nx.gnm_random_graph(
            self.number_of_nodes, number_of_edges, directed=True
        )
        return initial_network

    def create_initial_network_with_homophilic_attachment(self):
        initial_network = nx.DiGraph()
        initial_network.add_nodes_from(range(self.number_of_nodes))
        nodes_unsaturated = self.nodes.copy()
        while nodes_unsaturated:
            source = rd.choice(nodes_unsaturated)
            if rd.random() < self.probability_homophilic_attachment:
                if source in self.nodes_elite:
                    targets = self.nodes_elite.copy()
                else:
                    targets = self.nodes_mass.copy()
            else:
                if source in self.nodes_elite:
                    targets = self.nodes_mass.copy()
                else:
                    targets = self.nodes_elite.copy()

            non_targets: set = set(initial_network[source]).union({source})
            targets = list(set(targets).difference(non_targets))
            target = rd.choice(targets)
            initial_network.add_edge(source, target)

            # remove node from sources if it is already saturated
            if initial_network.out_degree(source) == self.degree:
                nodes_unsaturated.remove(source)
        return initial_network

    def rewire_network_using_preferential_attachment(self, initial_network):
        # Multi-type preferential attachment
        network = nx.DiGraph()
        network.add_nodes_from(range(self.number_of_nodes))
        edges_to_do = list(initial_network.edges()).copy()
        while edges_to_do:
            source, target = rd.choice(edges_to_do)
            # Define possible targets as nodes of the same type as target
            if target in self.nodes_elite:
                targets = self.nodes_elite.copy()
            else:
                targets = self.nodes_mass.copy()
            non_targets: set = set(network[source]).union({source})
            targets = list(set(targets).difference(non_targets))

            # Preferential attachment for targets of specified type
            population = list(
                network.in_degree(targets)
            )  # list of tuples of the form (node, in_degree of node)
            targets_in_degrees = list(map(lambda tuple_item: tuple_item[1], population))
            if rd.random() < self.probability_preferential_attachment:
                target_new = rd.choice(targets)
            else:
                if not targets:
                    break
                elif all(w == 0 for w in targets_in_degrees):
                    # catches the case where all weights are zero
                    target_new = rd.choice(targets)
                else:
                    target_new, target_new_in_degree = rd.choices(
                        population=population, weights=targets_in_degrees
                    )[0]
                    # Note on [0]: rd.choices produces a list
            # add edge to new network and remove edge from edges_to_do
            network.add_edge(source, target_new)
            edges_to_do.remove((source, target))
        return network

    def initialize_node_attributes(self):
        for elite_node in self.nodes_elite:
            self.network.nodes[elite_node]["type"] = "elite"
            self.network.nodes[elite_node]["competence"] = self.elite_competence
        for mass_node in self.nodes_mass:
            self.network.nodes[mass_node]["type"] = "mass"
            self.network.nodes[mass_node]["competence"] = self.mass_competence

    # TODO: estimated accuracy seems very inaccurate. Perhaps do binomial proportion
    #  confidence interval?
    def estimated_community_accuracy(self, number_of_voting_simulations):
        data = {"mass": 0, "elite": 0}
        for simulation in range(number_of_voting_simulations):
            vote_outcome = self.vote()
            data[vote_outcome] = data[vote_outcome] + 1
        estimated_accuracy = data["mass"] / (data["mass"] + data["elite"])
        return estimated_accuracy

    def estimated_community_accuracy_confidence_interval(
        self, number_of_voting_simulations, alpha: float = 0.05
    ):
        # TODO: check if we want to keep this
        data = {"mass": 0, "elite": 0}
        for simulation in range(number_of_voting_simulations):
            vote_outcome = self.vote()
            data[vote_outcome] = data[vote_outcome] + 1
        number_of_success = data["mass"]
        number_of_trials = data["mass"] + data["elite"]
        confidence_interval = proportion_confint(
            number_of_success, number_of_trials, alpha=alpha
        )
        return confidence_interval

    def vote(self):
        self.update_votes()
        list_of_votes = [self.network.nodes[node]["vote"] for node in self.nodes]
        majority_winner(list_of_votes)
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
                self.network.nodes[node_elite]["opinion"] = "elite"
            else:
                self.network.nodes[node_elite]["opinion"] = "mass"
        for node_mass in self.nodes_mass:
            if rd.random() < self.mass_competence:
                self.network.nodes[node_mass]["opinion"] = "mass"
            else:
                self.network.nodes[node_mass]["opinion"] = "elite"
