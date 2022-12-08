import os

from generate_figures_scripts.figure_accuracy_homophily import (
    figure_accuracy_homophilic,
)
from generate_figures_scripts.figure_distribution_accuracy import (
    figure_distribution_accuracy,
)
from generate_figures_scripts.figure_distribution_influence_proportion import (
    figure_distribution_influence,
)
from generate_figures_scripts.figure_epistemic_accuracy import figure_epistemic_accuracy

if __name__ == "__main__":
    folder_name = "new_figures"
    os.makedirs(folder_name, exist_ok=True)

    figure_accuracy_homophilic(
        filename=f"{folder_name}/figure_accuracy_homophilic",
        number_of_communities=200,
        number_of_voting_simulations=200,
    )
    figure_distribution_influence(
        filename=f"{folder_name}/figure_distribution_influence",
        data_file="data/clean.csv",
    )
    figure_distribution_accuracy(
        filename=f"{folder_name}/figure_distribution_accuracy",
        data_file="data/clean.csv",
    )
    figure_epistemic_accuracy(
        filename=f"{folder_name}/figure_epistemic_accuracy", scale=4
    )
