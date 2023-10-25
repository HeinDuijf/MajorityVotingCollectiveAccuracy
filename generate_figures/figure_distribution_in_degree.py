import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scripts.save_read_community import read_community_from_combined_file

cm = 1 / 2.54  # variable used to convert inches to cm


def figure_distribution_in_degree(
    filename: str = None, communities_file: str = None, collect: bool = True
):
    """Generates a plot of the in-degree distribution to verify that the generated
    communities are scale-free.

    The conclusion is that preferential attachment communities with number_of_nodes 100,
    degree 6 and probability_preferential_attachment 0.4 are scale-free, but this may
    not be the case for other parameter settings.

    Parameters
    ----------
    filename: str
        The filename of the plot
    communities_file: str
        The (pickle) file containing all communities
    collect: bool
        Boolean condition on whether the algorithm collects the in-degrees. This
        condition was included for the practical reason that collecting the in-degrees
        of 10**5 communities, of 100 agents each, can take a long time.

    Returns
    -------
        Plot of in-degree distribution """
    number_of_nodes: int = 100
    number_of_communities: int = 10 ** 5
    data = pd.DataFrame(columns=["degree", "frequency"])
    data["degree"] = np.arange(0, number_of_nodes + 1, 1, dtype=int)
    data["frequency"]: int = 0
    root_dir = (
        os.path.dirname(__file__).replace("\\", "/").removesuffix("generate_figures")
    )
    directory = os.path.dirname(communities_file)

    # 1. Collect data about the in-degrees in the generated communities
    if collect:
        for community_number in range(number_of_communities):
            community = read_community_from_combined_file(
                f"{communities_file}", community_number=community_number
            )
            for node in community.nodes:
                node_in_degree = community.network.in_degree(node)
                old_frequency = data.at[node_in_degree, "frequency"]
                data.at[node_in_degree, "frequency"] = old_frequency + 1
            print(
                f"Collected community {community_number} out of {number_of_communities}"
            )
        data["frequency"] = data["frequency"] / (
            number_of_communities * number_of_nodes
        )
        data.to_csv(f"{directory}/distribution_in_degrees.csv")

    # 2. Plot the in-degree distribution on log-log scale
    if not collect:
        data = pd.read_csv(f"{directory}/distribution_in_degrees.csv")
    data.plot.scatter(
        x="degree",
        y="frequency",
        loglog=True,
        legend=False,
        xlim=[1, 100],
        ylim=[10 ** -4, 1],
        title="In-degree distribution",
        ylabel="frequency",
        xlabel="in-degree",
        figsize=(14 * cm, 11 * cm),
        c="black",
    )
    if filename:
        filename = f"{root_dir}/{filename}"
        plt.savefig(fname=filename, dpi="figure")
    else:
        plt.show()


if __name__ == "__main__":
    figure_distribution_in_degree(
        collect=True,
        filename="../new_figures/figure_distribution_in_degrees",
        communities_file="../data/communities.pickle",
    )
