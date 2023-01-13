import pandas as pd
import statsmodels.api as sm
from basic_functions import convert_math_to_text


def table_variance_multiple_datasets(
    data_file: str = "data/clean.csv", output_file: str = None
):
    # Initialize
    df = pd.read_csv(data_file)

    output = "collective_accuracy"
    rows: list = [
        "p_e + p_m",
        "E",
        "I_e",
        "E + I_e",
        "p_e + p_m + E",
        "p_e + p_m + I_e",
        "p_e + p_m + E + I_e",
    ]
    table = pd.DataFrame(index=rows)

    # Setting variable range for subdata
    subdata_vars: dict = {
        "low": [0.55, 0.60],
        "med": [0.60, 0, 65],
        "high": [0.65, 0.70],
    }

    # Analysis
    for subdata_type in subdata_vars.keys():
        competence_range = subdata_vars[subdata_type]
        subdata = df.loc[
            (df["minority_competence"] > min(competence_range))
            & (df["minority_competence"] < max(competence_range))
            & (df["majority_competence"] > min(competence_range))
            & (df["majority_competence"] < max(competence_range))
        ]
        for row in rows:
            variables = convert_math_to_text(row)
            Y = subdata[output]
            X = subdata[variables]
            X = sm.add_constant(X)
            model = sm.OLS(Y, X).fit()
            table.loc[row, subdata_type] = round(model.rsquared, 3)

    if not output_file:
        return table
    else:
        table.to_csv(f"stats/{output_file}.csv")


if __name__ == "__main__":
    table_variance_multiple_datasets(output_file="test_table_multi")