import random as rd
import networkx as nx
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
            # Create network from edges.
            # TODO: this comment is obsolete, since the function name is perfect
            self.network = self.create_network_from_edges()
            return self.network

        # Create initial network.
        # TODO: this comment is also obsolete.
        # I would rename create_initial to initialize (a bit shorter)
        if self.probability_homophilic_attachment is None:
            # Create network without homophilic influence
            initial_network = (
                self.create_initial_network_without_homophilic_attachment()
            )
        else:
            initial_network = self.create_initial_network_with_homophilic_attachment()

        # Preferential rewiring.
        # TODO: This function name is also very long. I cannot find any other ways
        # of rewiring networks, so maybe self.rewire_network() would also be sufficient?
        # In that function you can explain the preferential attachment stuff
        self.network = self.rewire_network_using_preferential_attachment(
            initial_network
        )

        self.neighborhood = dict()
        for node in self.nodes:
            self.neighborhood[node] = list(self.network[node]) + [node]

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
        nodes_unsaturated = self.nodes.copy()
        # TODO: while loops are difficult to read, and sensitive for bugs and errors.
        # Sometimes they are necessary.
        # I think (not certain though) that in this case you could also have
        # created a for-loop over all nodes. That pattern would then also
        # resemble the for-loop in the other create_network function, which would be nice
        while nodes_unsaturated:
            source = rd.choice(nodes_unsaturated)

            if rd.random() < self.probability_homophilic_attachment:
                if source in self.nodes_elite:
                    nodes_same_type = self.nodes_elite.copy()
                else:
                    nodes_same_type = self.nodes_mass.copy()
            else:
                if source in self.nodes_elite:
                    nodes_same_type = self.nodes_mass.copy()
                else:
                    nodes_same_type = self.nodes_elite.copy()

            # TODO: I think the below script is better readable maybe
            # homophilic = rd.random() > self.probability_homophilic_attachment
            # source_elite = source in self.nodes_elite
            # if (homophilic and source_elite) | (not homophilic and not source_elite):
            #     nodes_same_type = self.nodes_mass
            # else:
            #     nodes_same_type = self.nodes_elite

            # TODO: you can immediately see that not_targets is a set
            non_targets: set = set(initial_network[source]).union({source})
            targets = list(set(nodes_same_type).difference(non_targets))
            target = rd.choice(targets)
            initial_network.add_edge(source, target)

            # remove node from sources if it is already saturated
            if initial_network.out_degree(source) == self.degree:
                nodes_unsaturated.remove(source)
        return initial_network

    def rewire_network_using_preferential_attachment(self, initial_network):
        # Initialize network and nodes
        network = nx.DiGraph()
        network.add_nodes_from(self.nodes)

        # Multi-type preferential attachment
        edges_to_do = list(initial_network.edges()).copy()
        # TODO: I again think the while loop is dangerous, and can be changed to for-loop
        while edges_to_do:
            source, target = rd.choice(edges_to_do)
            if target in self.nodes_elite:
                nodes_of_target_type = self.nodes_elite
            else:
                nodes_of_target_type = self.nodes_mass

            # TODO: converting to set is not necessary, since there is no duplication
            non_targets = list(network[source]) + [source]
            targets = [node for node in nodes_of_target_type if node not in non_targets]

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
                    target_new, _ = rd.choices(
                        population=population, weights=targets_in_degrees
                    )[0]
                    # Note on [0]: rd.choices produces a list
            # add edge to new network and remove edge from edges_to_do
            network.add_edge(source, target_new)
            edges_to_do.remove((source, target))
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
        number_of_success: int = 0
        # You could also rewrite:
        # vote_outcomes = [self.vote() for _ in range(number_of_voting_simulations)]
        # n_successes = len(outcome for outcome in vote_outcomes if outcome=='mass')
        for _ in range(number_of_voting_simulations):
            vote_outcome = self.vote()
            if vote_outcome == 0:
                number_of_success = number_of_success + 1
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
        elite_influence_counter = self.count_elite_influence()
        elite_votes = 0
        for node in elite_influence_counter:
            if elite_influence_counter[node] > self.degree / 2:
                elite_votes = elite_votes + 1
            elif elite_influence_counter[node] == self.degree / 2:
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
