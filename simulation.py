import random as rd

from community import Community


class Simulation:
    def __init__(
        self,
        file: str,
        number_of_communities: int,
        number_of_voting_simulations: int,
        number_of_nodes: int = 100,
        degree: int = 6,
        probability_preferential_attachment: float = 0.6,
        elite_competence_range=(0.55, 0.95),
        mass_competence_range=(0.55, 0.95),
        number_of_elites_range=(20, 45),
        probability_homophilic_attachment_range=(0.5, 1.0),
    ):
        self.file = file
        self.number_of_communities = number_of_communities
        self.number_of_voting_simulations = number_of_voting_simulations
        self.number_of_nodes = number_of_nodes
        self.degree = degree
        self.probability_preferential_attachment = probability_preferential_attachment
        self.elite_competence_range = elite_competence_range
        self.mass_competence_range = mass_competence_range
        self.number_of_elites_range = number_of_elites_range
        self.probability_homophilic_attachment_range = (
            probability_homophilic_attachment_range
        )

    def run(self):
        self.write_head_line()
        for community_number in range(self.number_of_communities):
            community = self.random_community()
            self.simulate_and_write_data_line(community)
            self.report_progress(community_number)
        print("The simulation is a great success.")

    def random_community(self):
        elite_competence: float = rd.uniform(*self.elite_competence_range)
        mass_competence: float = rd.uniform(*self.mass_competence_range)
        probability_homophilic_attachment: float = rd.uniform(
            *self.probability_homophilic_attachment_range
        )
        number_of_elites: int = rd.randint(*self.number_of_elites_range)

        # 1. Generate community with these parameters
        community = Community(
            number_of_nodes=self.number_of_nodes,
            number_of_elites=number_of_elites,
            degree=self.degree,
            elite_competence=elite_competence,
            mass_competence=mass_competence,
            probability_preferential_attachment=(
                self.probability_preferential_attachment
            ),
            probability_homophilic_attachment=probability_homophilic_attachment,
        )
        return community

    def write_head_line(self):
        head_line = (
            "collective_accuracy,"
            + "collective_accuracy_precision,"
            + "minority_competence, "
            + "majority_competence,"
            + "number_of_minority,"
            + "proportional_influence_minority,"
            + "homophily"
        )
        file = open(self.file, "w")
        file.write(f"{head_line}")
        file.close()

    def simulate_and_write_data_line(self, community: Community):
        # Gather parameters
        minority_competence = community.elite_competence
        majority_competence = community.mass_competence
        number_of_minority = community.number_of_elites
        homophily = community.probability_homophilic_attachment
        total_influence_minority = community.total_influence_elites()
        total_influence_majority = community.total_influence_mass()
        proportional_influence_minority = total_influence_minority / (
            total_influence_minority + total_influence_majority
        )
        # Run voting simulations to estimate accuracy
        result = community.estimated_community_accuracy(
            self.number_of_voting_simulations
        )
        collective_accuracy = result["estimated_accuracy"]
        collective_accuracy_precision = result["precision"]

        # Print results to line in csv file
        data_line = (
            f"{collective_accuracy}, {collective_accuracy_precision}, "
            f"{minority_competence}, {majority_competence}, {number_of_minority}, "
            f"{proportional_influence_minority}, {homophily}"
        )
        file = open(self.file, "a")
        file.write(f"\n{data_line}")
        file.close()

    def report_progress(self, community_number):
        if community_number % (self.number_of_communities / 100) == 0:
            progress = int((community_number * 100) / self.number_of_communities)
            print(f"Progress simulation run: {progress}%")
