import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

""" Parameter settings """
font_style: dict = {"family": "Calibri", "size": 11}
cm = 1 / 2.54  # variable used to convert inches to cm
histogram_size = (14 * cm, 10 * cm)
line_plot_size = (14 * cm, 10.5 * cm)


def histogram_plot(
    dataframe: pd.DataFrame,
    title: str,
    xlabel: str,
    ylabel_left: str,
    ylabel_right: str,
    xlim=(0.3, 0.6),
    xticks=0.3 + 0.1 * np.arange(0, 4, 1, dtype=int),
    ylim=(0, 1),
    filename: str = None,
):
    # Initialize style parameters
    plt.rc("font", **font_style)

    # Plot histogram
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=histogram_size)
    ax.hist(
        dataframe["influence_minority_proportion"],
        bins=30,
        color="white",
        edgecolor="gray",
    )
    ax_cumulative = ax.twinx()
    ax.set(
        title=title, ylabel=ylabel_left, xlabel=xlabel, xlim=xlim, xticks=xticks,
    )
    ax.yaxis.label.set_color("gray")
    ax.tick_params(axis="y", colors="gray")

    # Cumulative line plot
    y_values, x_values = np.histogram(
        dataframe["influence_minority_proportion"], bins=30, range=xlim
    )
    y_values = np.cumsum(y_values)
    y_values = 1 / np.max(y_values) * y_values
    x_values = x_values[:-1]
    ax_cumulative.plot(x_values, y_values, color="black")
    ax_cumulative.set(ylabel=ylabel_right, ylim=ylim)

    # Mean and standard deviation
    data_mean = dataframe["influence_minority_proportion"].mean()
    data_std = dataframe["influence_minority_proportion"].std()
    plt.axvline(data_mean, color="black", linestyle="dashed")
    plt.axvline(data_mean + data_std, color="black", linestyle="dotted")
    plt.axvline(data_mean - data_std, color="black", linestyle="dotted")

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
    # Initialize style parameters
    plt.rc("font", **font_style)
    colormap = sns.color_palette("crest", as_cmap=True)

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
