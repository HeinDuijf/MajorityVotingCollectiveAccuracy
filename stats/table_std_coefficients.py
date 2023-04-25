import pandas as pd
import statsmodels.api as sm
from scipy import stats
from scripts.basic_functions import convert_math_to_text


def table_std_coefficients(data_file: str = "data/clean.csv", output_file: str = None):
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

    for subdata_key in subdata_vars.keys():
        competence_range = subdata_vars[subdata_key]
        df_sub = df.loc[
            (df["minority_competence"] > min(competence_range))
            & (df["minority_competence"] < max(competence_range))
            & (df["majority_competence"] > min(competence_range))
            & (df["majority_competence"] < max(competence_range))
        ]

        # Standardized coefficients
        variables = [convert_math_to_text(row) for row in rows]
        df_norm = pd.DataFrame(stats.zscore(df_sub))
        Y_norm = df_norm[output]
        X_norm = df_norm[variables]
        X_norm = sm.add_constant(X_norm)
        model_norm = sm.OLS(Y_norm, X_norm).fit()
        for row in rows:
            variable = convert_math_to_text(row)
            table.loc[row, subdata_key] = round(model_norm.params[variable], 3)

    if not output_file:
        return table
    else:
        table.to_csv(f"stats/{output_file}.csv")


if __name__ == "__main__":
    table_std_coefficients(output_file="test_std_coeff")
