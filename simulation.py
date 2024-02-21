import concurrent.futures as cf
import os
import random as rd
import shutil
import time

from community import Community
from scripts.basic_functions import calculate_accuracy_and_precision
from scripts.save_read_community import combine_community_files, save_community_to_file


class Simulation:
    def __init__(
        self,
        folder_communities: str,
        filename_csv: str,
        number_of_communities: int,
        number_of_voting_simulations: int,
        number_of_nodes: int = 100,
        degree: int = 6,
        probability_preferential_attachment: float = 0.6,
        elite_competence_range=(0.55, 0.7),
        mass_competence_range=(0.55, 0.7),
        number_of_elites_range=(25, 45),
        probability_homophilic_attachment_range=None,
        probability_competence_selection_range=None,
    ):
        self.start_time = time.time()
        self.filename_csv = f"{filename_csv}.csv"
        self.folder_communities = folder_communities
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
        self.probability_competence_selection_range = (
            probability_competence_selection_range
        )

    def run(self):
        print(f"Started simulation at {time.ctime()}")
        self.start_time = time.time()
        self.initialize_dirs()
        self.write_readme()
        self.write_head_line()
        with cf.ProcessPoolExecutor() as executor:
            executor.map(self.single_run, range(self.number_of_communities))
        combine_community_files(
            directory_path=f"{self.folder_communities}/communities",
            output_file=f"{self.folder_communities}/communities.pickle",
            delete_directory=False,
        )
        # for community_number in range(self.number_of_communities):
        #     self.single_run(number=community_number)
        print("The simulation is a great success.")

    def single_run(self, number: int):
        community = self.generate_community()
        save_community_to_file(
            filename=f"{self.folder_communities}/communities/{number}",
            community=community,
        )
        self.simulate_and_write_data_line(community=community, number=number)
        self.report_progress(number)

    def initialize_dirs(self):
        if os.path.exists(f"{self.folder_communities}"):
            shutil.rmtree(f"{self.folder_communities}")
        os.makedirs(f"{self.folder_communities}", exist_ok=True)
        os.makedirs(f"{self.folder_communities}/communities", exist_ok=True)
        if os.path.exists(f"{self.filename_csv}"):
            os.remove(f"{self.filename_csv}")

    def write_readme(self):
        information = (
            f"parameter, value\n"
            f"filename, {self.filename_csv}\n"
            f"folder, {self.folder_communities}\n"
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
            f"{self.probability_homophilic_attachment_range}\n"
            f"probability_competence_selection_range, "
            f"{self.probability_competence_selection_range}"
        )
        filename_readme = f"{self.folder_communities}/README.csv"
        with open(filename_readme, "w") as f:
            f.write(information)

    def generate_community(self):
        elite_competence: float = rd.uniform(*self.elite_competence_range)
        mass_competence: float = rd.uniform(*self.mass_competence_range)

        if self.probability_homophilic_attachment_range is not None:
            probability_homophilic_attachment = rd.uniform(
                *self.probability_homophilic_attachment_range
            )
        else:
            probability_homophilic_attachment = None

        if self.probability_competence_selection_range is not None:
            probability_competence_selection = rd.uniform(
                *self.probability_competence_selection_range
            )
        else:
            probability_competence_selection = None

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
            probability_competence_selection=probability_competence_selection,
        )
        return community

    def write_head_line(self):
        head_line = (
            "community_number,"
            + "minority_competence,"
            + "majority_competence,"
            + "number_of_minority,"
            + "influence_minority_proportion,"
            + "homophily,"
            + "competence_selection,"
            + "accuracy,"
            + "accuracy_precision,"
            + "accuracy_pre_influence,"
            + "accuracy_precision_pre_influence,"
            + "mean,"
            + "median,"
            + "std,"
            + "mean_pre_influence,"
            + "median_pre_influence,"
            + "std_pre_influence"
        )
        with open(self.filename_csv, "w") as f:
            f.write(head_line)

    def simulate_and_write_data_line(self, community: Community, number: int):
        # Determine influence_minority_proportion
        total_influence_minority = community.total_influence_elites()
        total_influence_majority = community.total_influence_mass()
        influence_minority_proportion = total_influence_minority / (
            total_influence_minority + total_influence_majority
        )
        # Run voting simulations to estimate accuracy
        result = community.voting_simulation(self.number_of_voting_simulations)
        accuracy = result["accuracy"]
        accuracy_precision = result["precision"]
        accuracy_pre_influence = result["accuracy_pre_influence"]
        accuracy_precision_pre_influence = result["precision_pre_influence"]
        mean = result["mean"]
        median = result["median"]
        std = result["std"]
        mean_pre_influence = result["mean_pre_influence"]
        median_pre_influence = result["median_pre_influence"]
        std_pre_influence = result["std_pre_influence"]

        # Print results to line in csv folder_communities
        data_line = (
            f"{number},{community.elite_competence},{community.mass_competence},"
            f"{community.number_of_elites},{influence_minority_proportion},"
            f"{community.probability_homophilic_attachment},"
            f"{community.probability_competence_selection},{accuracy},"
            f"{accuracy_precision},{accuracy_pre_influence},"
            f"{accuracy_precision_pre_influence},{mean},{median},{std},"
            f"{mean_pre_influence},{median_pre_influence},{std_pre_influence}"
        )
        with open(self.filename_csv, "a") as f:
            f.write(f"\n{data_line}")

    def report_progress(self, community_number):
        stamps_percent = [1, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90]
        stamps_numbers = [
            (percent / 100) * self.number_of_communities for percent in stamps_percent
        ]
        if community_number in stamps_numbers:
            progress = int((community_number * 100) / self.number_of_communities)
            current_time_sec = time.time()
            elapsed_time_sec = current_time_sec - self.start_time
            estimated_total_time_sec = (elapsed_time_sec / progress) * 100
            estimated_finish_time_sec = self.start_time + estimated_total_time_sec
            estimated_finish_time_clock = time.ctime(estimated_finish_time_sec)
            print(
                f"Progress: {progress}%\n"
                f"Estimated finish time: {estimated_finish_time_clock}"
            )


if __name__ == "__main__":
    Simulation(
        folder_communities="data/test_competence",
        filename_csv="data/test_competence",
        number_of_communities=10**4,
        number_of_voting_simulations=10**4,
        number_of_nodes=10**2,
        number_of_elites_range=(6, 20),
        elite_competence_range=(0.6, 0.8),
        mass_competence_range=(0.5, 0.6),
        probability_competence_selection_range=(0.5, 0.9),
    ).run()
