import pandas as pd

from generate_figures.figure_basics import cumulative_line_plot


def figure_cumulative_prior_post(
    filename: str = None, data_file: str = "data/clean.csv"
):
    df = pd.read_csv(data_file)

    cumulative_line_plot(dataframe=df, filename=filename)


if __name__ == "__main__":
    figure_cumulative_prior_post(data_file="../data/clean.csv")
