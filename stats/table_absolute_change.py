import pandas as pd
import statsmodels.api as sm
from scripts.basic_functions import convert_math_to_text


def table_absolute_change(data_file: str = "data/clean.csv", output_file: str = None):
    # Initialize
    df = pd.read_csv(data_file)

    output = "collective_accuracy"
    rows: list = ["p_e", "p_m", "E", "I_e"]
    table = pd.DataFrame(index=rows)

    # Setting variable range for subdata
    subdata_vars: dict = {
        "full": [0, 1],
        "low": [0.55, 0.60],
        "med": [0.60, 0.65],
        "high": [0.65, 0.70],
    }

    for subdata_type in subdata_vars.keys():
        competence_range = subdata_vars[subdata_type]
        subdata = df.loc[
            (df["minority_competence"] > min(competence_range))
            & (df["minority_competence"] < max(competence_range))
            & (df["majority_competence"] > min(competence_range))
            & (df["majority_competence"] < max(competence_range))
        ]

        # Standardized coefficients
        variables = [convert_math_to_text(row) for row in rows]
        Y = subdata[output]
        X = subdata[variables]
        X = sm.add_constant(X)
        model = sm.OLS(Y, X).fit()
        for row in rows:
            variable = convert_math_to_text(row)
            variable_coef = model.params[variable]
            variable_change = 0.05 / variable_coef
            if row == "E":
                table.loc[row, subdata_type] = int(variable_change)
            else:
                table.loc[row, subdata_type] = round(variable_change, 3)
    if not output_file:
        return table
    else:
        table.to_csv(f"stats/{output_file}.csv")


if __name__ == "__main__":
    table_absolute_change(output_file="test_abs_change")
