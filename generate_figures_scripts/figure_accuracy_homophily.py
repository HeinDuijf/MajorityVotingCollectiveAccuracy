import numpy as np
import pandas as pd
from community import Community

from generate_figures_scripts.figure_basics import line_plot


def figure_accuracy_homophilic(
    filename: str = None,
    number_of_nodes: int = 100,
    degree: int = 6,
    number_of_elites: int = 40,
    number_of_communities: int = 200,
    number_of_voting_simulations: int = 100,
):
    """Plots the collective accuracy in communities of a certain type for various
    competences and degrees of homophily.

    Parameters
    ----------
    filename
        Saves figure in 'filename' or shows figure if 'filename' is not given
    number_of_nodes
        Number of nodes
    degree
        Degree of the network
    number_of_elites: int
        Number of elites
    number_of_communities: int
        Number of communities used for each data point
    number_of_voting_simulations: int
        Number of steps used to estimate collective accuracy in each network

    Returns
    ----------
    Plot of collective accuracy for various competences and degrees of homophily"""
    # Initialize variables
    homophily_values = 0.1 * np.arange(0, 6, 1, dtype=int) + 0.5
    competence_values = 0.05 * np.arange(0, 4, 1, dtype=int) + 0.55
    columns = ["homophily", "competence", "accuracy"]
    df = pd.DataFrame(columns=columns)

    # Get data points
    for counter, h in enumerate(homophily_values):
        for c in competence_values:
            c = round(c, 2)
            # Collect data about the accuracy in generated communities
            for community_number in range(number_of_communities):
                community = Community(
                    number_of_nodes=number_of_nodes,
                    number_of_elites=number_of_elites,
                    degree=degree,
                    elite_competence=c,
                    mass_competence=c,
                    probability_homophilic_attachment=h,
                )
                result = community.estimated_community_accuracy(
                    number_of_voting_simulations=number_of_voting_simulations
                )
                e = result["accuracy"]
                data_line = pd.DataFrame(data=[[h, c, e]], columns=columns)
                df = pd.concat([df, data_line], ignore_index=True)
        progress = int(100 * ((counter + 1) / len(homophily_values)))
        print(f"Progress figure_accuracy_homophilic: {progress}%")

    # 3. Plot
    ylabel = "collective accuracy"
    xlabel = "homophily value"
    xlim = (0.5, 1)
    ylim = (0.5, 0.85)
    title = (
        f"Collective accuracy in scale-free communities \nwith homophilic "
        f"influence and {number_of_elites}% minority"
    )
    line_plot(
        filename=filename,
        dataframe=df,
        x="homophily",
        y="accuracy",
        hue="competence",
        title=title,
        ylabel=ylabel,
        xlabel=xlabel,
        xlim=xlim,
        ylim=ylim,
    )


if __name__ == "__main__":
    figure_accuracy_homophilic(
        number_of_communities=10, number_of_voting_simulations=10
    )
