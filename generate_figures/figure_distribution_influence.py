import numpy as np
import pandas as pd
from figures.figure_basics import histogram_plot

# from definitions import ROOT_DIR


def figure_distribution_influence(
    filename: str = None, data_file: str = "data/clean.csv"
):
    """Plots the distribution of the proportional influence of the minority and the cumulative lineplot.

    Parameters
    ----------

    Returns
    -------
        Plot of the distribution of proportional influence of the minority and the
        cumulative lineplot
    """
    # data_file = f"{ROOT_DIR}/{data_file}"
    df = pd.read_csv(data_file)

    # Histogram
    histogram_plot(
        filename=filename,
        dataframe=df,
        title="Distribution of the proportional\n influence of the minority",
        ylabel_left="number of occurrences",
        xlabel="proportional influence minority",
        xlim=(0.3, 0.6),
        xticks=0.3 + 0.1 * np.arange(0, 4, 1, dtype=int),
        ylabel_right="cumulative probability",
        ylim=(0, 1),
    )


if __name__ == "__main__":
    figure_distribution_influence()
