import pandas as pd


def correlations(data_file: str = "data/clean.csv", output_file: str = None):
    # Initialize
    df = pd.read_csv(data_file)

    independent_variables = [
        "minority_competence",
        "majority_competence",
        "number_of_minority",
        "homophily",
        "influence_minority_proportion",
    ]
    table = df[independent_variables].corr()

    if not output_file:
        return table
    else:
        table.to_csv(f"stats/{output_file}.csv")
