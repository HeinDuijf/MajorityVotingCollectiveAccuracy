import concurrent.futures as cf
import multiprocessing
import os
import random as rd

from community import Community
from save_read_community import read_community_from_file, save_community_to_file


class Simulation:
    def __init__(
        self,
        folder: str,
        filename: str,
        number_of_communities: int,
        number_of_voting_simulations: int,
        number_of_nodes: int = 100,
        degree: int = 6,
        probability_preferential_attachment: float = 0.6,
        elite_competence_range=(0.55, 0.7),
        mass_competence_range=(0.55, 0.7),
        number_of_elites_range=(25, 45),
        probability_homophilic_attachment_range=(0.5, 0.75),
    ):
        self.filename = filename
        self.folder = folder
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
        os.makedirs(f"{self.folder}", exist_ok=True)
        self.write_readme()
        self.write_head_line()
        with cf.ProcessPoolExecutor() as executor:
            executor.map(self.single_run, range(self.number_of_communities))
        # for community_number in range(self.number_of_communities):
        #     self.single_run(number=community_number)
        print("The simulation is a great success.")

    def single_run(self, number: int):
        community = self.generate_community()
        save_community_to_file(
            filename=f"{self.folder}/communities/{number}", community=community
        )
        self.simulate_and_write_data_line(community=community, number=number)
        progress_message = "Progress"
        self.report_progress(progress_message, number)

    def run_simulations_and_save_results_to_csv(self):
        self.write_head_line()
        for community_number in range(self.number_of_communities):
            community = read_community_from_file(
                f"{self.folder}/communities/{community_number}"
            )
            self.simulate_and_write_data_line(community)
            progress_message = "Progress voting simulations and saving results"
            self.report_progress(progress_message, community_number)
        print(
            f"The simulation involving the communities in folder {self.folder} is a "
            f"great success."
        )

    def write_readme(self):
        information = (
            f"parameter, value\n"
            f"filename, {self.filename}\n"
            f"folder, {self.folder}\n"
            f"number_of_communities, {self.number_of_communities}\n"
            f"number_of_voting_simulations, {self.number_of_voting_simulations}\n"
            f"number_of_nodes, {self.number_of_nodes}\n"
            f"degree, {self.degree}\n"
            f"probability_preferential_attachment"
            f", {self.probability_preferential_attachment}\n"
            f"elite_competence_range, {self.elite_competence_range}\n"
            f"mass_competence_range, {self.mass_competence_range}\n"
            f"number_of_elites_range, {self.number_of_elites_range}\n"
            f"probability_homophilic_attachment_range, "
            f"{self.probability_homophilic_attachment_range}"
        )
        filename_readme = f"{self.folder}/README.csv"
        with open(filename_readme, "w") as f:
            f.write(information)

    def generate_community(self):
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
            "community_number,"
            + "collective_accuracy,"
            + "collective_accuracy_precision,"
            + "minority_competence,"
            + "majority_competence,"
            + "number_of_minority,"
            + "influence_minority_proportion,"
            + "homophily"
        )
        with open(self.filename, "w") as f:
            f.write(head_line)

    def simulate_and_write_data_line(self, community: Community, number: int):
        # Determine influence_minority_proportion
        total_influence_minority = community.total_influence_elites()
        total_influence_majority = community.total_influence_mass()
        influence_minority_proportion = total_influence_minority / (
            total_influence_minority + total_influence_majority
        )
        # Run voting simulations to estimate accuracy
        result = community.estimated_community_accuracy(
            self.number_of_voting_simulations
        )
        collective_accuracy = result["accuracy"]
        collective_accuracy_precision = result["precision"]

        # Print results to line in csv folder
        data_line = (
            f"{number}, {collective_accuracy}, {collective_accuracy_precision}, "
            f"{community.elite_competence}, {community.mass_competence}, "
            f"{community.number_of_elites}, {influence_minority_proportion}, "
            f"{community.probability_homophilic_attachment}"
        )
        with open(self.filename, "a") as f:
            f.write(f"\n{data_line}")

    def report_progress(self, message, community_number):
        if community_number % (self.number_of_communities / 100) == 0:
            progress = int((community_number * 100) / self.number_of_communities)
            print(f"{message}: {progress}%")
