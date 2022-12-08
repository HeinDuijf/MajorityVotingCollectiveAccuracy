import numpy as np
import pandas as pd
from scipy.stats import binom

from generate_figures_scripts.figure_basics import line_plot

# cm = 1 / 2.54  # variable used to convert inches to cm
# line_plot_size = (14 * cm, 10.5 * cm)
# font_style = {"family": "Calibri", "size": 11}


def epistemic_accuracy(group_size: int, competence: float):
    """ Function returns the epistemic accuracy of majority voting in a group of size
    'group_size' where each agent has competence 'competence'.

    Parameters
    ----------
    group_size: int
        The number of agents
    competence: float
        Competence level of agents

    Returns
    -------
    probability_right: float
        The probability that majority voting succeeds in selecting the correct
        alternative"""
    # 0. Initialize variables
    probability_correct: float = 0

    # 1. Calculate epistemic accuracy
    if (group_size % 2) == 0:
        # 1.a. Case where group_size is even and there can be ties.
        probability_more_than_half_correct = binom.sf(
            group_size / 2, group_size, competence
        )
        probability_tie = binom.pmf(group_size / 2, group_size, competence)
        probability_correct_after_tie = probability_tie / 2

        probability_correct = (
            probability_more_than_half_correct + probability_correct_after_tie
        )
        return probability_correct

    else:
        # 1.b. Case where group_size is odd and there can be no ties.
        probability_correct = binom.sf(group_size / 2, group_size, competence)
        return probability_correct


def figure_epistemic_accuracy(scale: int = 3, filename: str = None):
    """ Generates plot of the epistemic accuracy for various group sizes and competence
    levels.

    Parameters
    ----------
    scale: int
        Determines the range of group sizes where the upper limit equals 10**scale
    filename: str
        Location where the plot is to be saved

    Returns
    -------
        Plot of epistemic accuracy"""
    # 0. Initialize variables
    competence_values = [0.51, 0.55, 0.6, 0.7]
    initial_group_size_values = np.arange(1, 10, 1, dtype=int)
    group_size_values = initial_group_size_values
    for k in np.arange(1, scale + 1, dtype=int):
        group_size_values = np.hstack(
            (group_size_values, initial_group_size_values * 10 ** k + 1)
        )

    # 1. Plots
    columns = ["competence", "group_size", "accuracy"]
    df = pd.DataFrame(columns=columns)
    for competence in competence_values:
        for group_size in group_size_values:
            accuracy = epistemic_accuracy(group_size=group_size, competence=competence)
            data_line = pd.DataFrame(
                data=[[competence, group_size, accuracy]], columns=columns
            )
            df = pd.concat([df, data_line], ignore_index=True)

    line_plot(
        dataframe=df,
        x="group_size",
        y="accuracy",
        hue="competence",
        title="Epistemic accuracy of majority voting",
        ylabel="Epistemic accuracy",
        xlabel="Group size",
        ylim=(0.5, 1.0),
        xlim=(0, 10 ** scale),
    )


if __name__ == "__main__":
    figure_epistemic_accuracy(scale=4)
