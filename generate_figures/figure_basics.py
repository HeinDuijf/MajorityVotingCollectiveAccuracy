import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

""" Parameter settings """
font_style: dict = {"family": "Calibri", "size": 11}
cm = 1 / 2.54  # variable used to convert inches to cm
histogram_size = (14 * cm, 10 * cm)
line_plot_size = (14 * cm, 10.5 * cm)
plt.rc("font", **font_style)
colormap = sns.color_palette("rocket_r", as_cmap=True)  # Greys_d, crest,
palette = sns.color_palette("pink")
sns.set_style("whitegrid")


def histogram_plot(
    dataframe: pd.DataFrame,
    y: str,
    title: str,
    xlabel: str,
    ylabel_left: str,
    ylabel_right: str,
    xlim=(0.3, 0.6),
    xticks=0.3 + 0.1 * np.arange(0, 4, 1, dtype=int),
    ylim=(0, 1),
    filename: str = None,
):
    sns.set_style("white")
    # Plot histogram
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=histogram_size)

    sns.histplot(
        dataframe[y],
        element="bars",
        color="silver",
        bins=40,
        cumulative=False,
        stat="count",
        common_norm=False,
        ax=ax,
    )

    # Plot cumulative
    sns.set_style("whitegrid")
    ax_cumulative = ax.twinx()
    sns.histplot(
        dataframe[y],
        element="poly",
        color="dimgray",
        cumulative=True,
        stat="percent",
        common_norm=False,
        ax=ax_cumulative,
    )

    ax.set(
        title=title, ylabel=ylabel_left, xlabel=xlabel, xlim=xlim, xticks=xticks,
    )
    # ax.yaxis.label.set_color("gray")
    # ax.tick_params(axis="y", colors="gray")

    if filename:
        plt.savefig(fname=filename, dpi="figure")
    else:
        plt.show()


def line_plot(
    dataframe: pd.DataFrame,
    x: str,
    y: str,
    hue: str,
    title: str,
    xlabel: str,
    ylabel: str,
    xlim=(0.5, 1),
    ylim=(0.5, 0.85),
    filename: str = None,
):
    # Plot line
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=line_plot_size)
    sns.lineplot(
        data=dataframe, x=x, y=y, hue=hue, palette=colormap, legend="full",
    )
    ax.set(
        ylabel=ylabel, xlabel=xlabel, xlim=xlim, ylim=ylim, title=title,
    )

    # Show or save
    if filename:
        plt.savefig(fname=filename, dpi="figure")
    else:
        plt.show()


def cumulative_line_plot(
    dataframe: pd.DataFrame, filename: str = None,
):
    df = dataframe.melt()
    df = df[
        (df["variable"] == "accuracy") | (df["variable"] == "accuracy_pre_influence")
    ]
    df.columns = ["Type", "Accuracy"]
    df.replace("accuracy_pre_influence", "prior", inplace=True)
    df.replace("accuracy", "posterior", inplace=True)

    fig, ax = plt.subplots(figsize=histogram_size)
    sns.histplot(
        df,
        x="Accuracy",
        hue="Type",
        element="poly",
        cumulative=True,
        stat="percent",
        common_norm=False,
        palette=palette,
        ax=ax,
    )

    xticks = 0.1 * np.arange(0, 11, 1, dtype=int)
    yticks = 10 * np.arange(0, 11, 1, dtype=int)
    ylim = (0, 100)
    ax.set(ylim=ylim, yticks=yticks, xlim=(0, 1), xticks=xticks)
    ax.legend(["prior", "posterior"], loc="upper left")
    ax.set_title("Majoritarian accuracy: cumulative distributions", fontsize=16)

    # Show or save
    if filename:
        plt.savefig(
            fname="new_figures/figure_cumulative_prior_and_posterior", dpi="figure"
        )
    else:
        plt.show()
