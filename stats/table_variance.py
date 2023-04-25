import pandas as pd
import statsmodels.api as sm
from scripts.basic_functions import convert_math_to_text


def table_variance(data_file: str = "data/clean.csv", output_file: str = None):
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

    # Analysis
    for row in rows:
        # construct multiple linear regression model
        variables = convert_math_to_text(row)
        Y = df[output]
        X = df[variables]
        X = sm.add_constant(X)
        model = sm.OLS(Y, X).fit()
        table.loc[row, "R_squared"] = round(model.rsquared, 3)
    if not output_file:
        return table
    else:
        table.to_csv(f"stats/{output_file}.csv")


if __name__ == "__main__":
    table_variance(output_file="test_table")
