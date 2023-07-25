import math

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
from scripts.basic_functions import convert_math_to_text


def table_all_regressions(data_file: str = "data/clean.csv", output_file: str = None):
    # Initialize
    df = pd.read_csv(data_file)

    # Initialization
    independent_variables = [
        "minority_competence",
        "majority_competence",
        "number_of_minority",
        "homophily",
        "influence_minority_proportion",
    ]
    columns_initial = independent_variables
    columns = columns_initial.copy()
    for column in columns_initial:
        k = columns.index(column)
        columns[k : k + 1] = (
            f"{column}_p_value",
            f"{column}_coeff",
            f"{column}_coeff_std",
        )
    output = "collective_accuracy"
    rows: list = [
        "p_e + p_m",
        "E",
        "I_e",
        "E + I_e",
        "p_e + p_m + E",
        "p_e + p_m + I_e",
        "p_e + p_m + E + I_e",
        "p_e + p_m + h",
        "p_e + p_m + h + E",
        "p_e + p_m + h + I_e",
        "p_e + p_m + h + E + I_e",
    ]

    table = pd.DataFrame(index=rows, columns=columns)

    # Analysis
    for row in rows:
        # construct multiple linear regression model
        variables = convert_math_to_text(row)

        Y = df[output]
        X = df[variables]
        X = sm.add_constant(X)
        model = sm.OLS(Y, X).fit()

        # R-value, model error and F-value
        Y_pred = model.predict(X)
        mean_square_error = np.square(np.subtract(Y, Y_pred)).mean()
        root_mean_square_error = math.sqrt(mean_square_error)
        table.loc[row, "R_squared"] = round(model.rsquared, 3)
        table.loc[row, "R_squared (adj)"] = round(model.rsquared_adj, 3)
        table.loc[row, "root mean square error"] = round(root_mean_square_error, 3)
        table.loc[row, "F value"] = round(model.fvalue)

        # p-value, coefficients and standardized coefficients
        df_norm = pd.DataFrame(stats.zscore(df))
        Y_norm = df_norm[output]
        X_norm = df_norm[variables]
        X_norm = sm.add_constant(X_norm)
        model_norm = sm.OLS(Y_norm, X_norm).fit()

        for variable in variables:
            column_p = f"{variable}_p_value"
            table.loc[row, column_p] = round(model.pvalues[variable], 4)
            column_c = f"{variable}_coeff"
            table.loc[row, column_c] = round(model.params[variable], 4)
            column_cstd = f"{variable}_coeff_std"
            table.loc[row, column_cstd] = round(model_norm.params[variable], 4)

    if not output_file:
        return table
    else:
        table.to_csv(f"stats/{output_file}.csv")


if __name__ == "__main__":
    table_all_regressions(
        data_file="../data/clean.csv", output_file="test_table_all_regressions",
    )
