import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import binom

cm = 1 / 2.54  # variable used to convert inches to cm
line_plot_size = (14 * cm, 10.5 * cm)
font_style = {"family": "Calibri", "size": 11}


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
        The probability that majority voting succeeds in selecting the correct alternative"""
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
    competence_max = max(competence_values) + 0.1
    competence_range = competence_max - min(competence_values)

    # Scale group size values
    initial_values = np.arange(1, 10, 1, dtype=int)
    group_size_values = initial_values
    for k in np.arange(1, scale + 1, dtype=int):
        group_size_values = np.hstack((group_size_values, initial_values * 10 ** k + 1))

    # 1. Plots
    df = pd.DataFrame(index=group_size_values, columns=competence_values)
    for competence in competence_values:
        for group_size in group_size_values:
            df.at[group_size, competence] = epistemic_accuracy(
                group_size=group_size, competence=competence
            )

    title = "Epistemic accuracy of majority voting"
    ylabel = "Epistemic accuracy ($P(n, p_c)$)"
    xlabel = "Group size ($n$)"
    ylim = (0.5, 1.0)
    xlim = (0, 10 ** scale)
    cmap = plt.get_cmap("Greys")
    plt.rcParams.update(
        {"font.family": font_style["family"], "font.size": font_style["size"]}
    )
    df.plot(
        kind="line",
        title=title,
        xlabel=xlabel,
        ylabel=ylabel,
        figsize=line_plot_size,
        colormap=cmap,  # TODO: Fix colormap: one line is invisible.
        # xticks=xticks,
        xlim=xlim,
        ylim=ylim,
    )
    legend = [f"Competence {competence}" for competence in competence_values]
    plt.legend(legend, loc="lower right")

    if filename:
        plt.savefig(fname=filename, dpi="figure")
    else:
        plt.show()


figure_epistemic_accuracy(scale=4)
