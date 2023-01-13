import math

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import linalg, stats

from basic_functions import convert_math_to_text

# from sklearn.linear_model import LinearRegression
# import seaborn as sns
# import matplotlib.pyplot as plt


independent_variables = [
    "minority_competence",
    "majority_competence",
    "number_of_minority",
    "homophily",
    "influence_minority_proportion",
]


def correlations(dataframe):
    return dataframe[independent_variables].corr()


def table_variance(data_file: str = "data/clean.csv", filename: str = None):
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
    if not filename:
        return table
    else:
        print("yay")
        table.to_csv(f"stats/{filename}.csv")


def table_variance_multiple_datasets(
    data_file: str = "data/clean.csv", filename: str = None
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

    if not filename:
        return table
    else:
        table.to_csv(f"stats/{filename}.csv")


table_variance_multiple_datasets(filename="test_table_multi")


def table_std_coefficients(data_file: str = "data/clean.csv", filename: str = None):
    # Initialize
    df = pd.read_csv(data_file)

    output = "collective_accuracy"
    rows: list = ["p_e", "p_m", "E", "I_e"]
    table = pd.DataFrame(index=rows)

    # Setting variable range for subdata
    subdata_vars: dict = {
        "full": [0, 1],
        "low": [0.55, 0.60],
        "med": [0.60, 0, 65],
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
        df_norm = pd.DataFrame(stats.zscore(df))
        Y_norm = df_norm[output]
        X_norm = df_norm[variables]
        X_norm = sm.add_constant(X_norm)
        model_norm = sm.OLS(Y_norm, X_norm).fit()
        for row in rows:
            variable = convert_math_to_text(row)
            table.loc[rows, subdata_type] = round(model_norm.params[variable], 4)
    if not filename:
        return table
    else:
        table.to_csv(f"stats/{filename}.csv")


table_std_coefficients(filename="test_std_coeff")


def table_absolute_change(data_file: str = "data/clean.csv", filename: str = None):
    # Initialize
    df = pd.read_csv(data_file)

    output = "collective_accuracy"
    rows: list = ["p_e", "p_m", "E", "I_e"]
    table = pd.DataFrame(index=rows)

    # Setting variable range for subdata
    subdata_vars: dict = {
        "full": [0, 1],
        "low": [0.55, 0.60],
        "med": [0.60, 0, 65],
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
        Y = df[output]
        X = df[variables]
        X = sm.add_constant(X)
        model = sm.OLS(Y, X).fit()
        for row in rows:
            variable = convert_math_to_text(row)
            variable_coef = model.params[variable]
            table.loc[rows, subdata_type] = round(0.05 / variable_coef, 4)
    if not filename:
        return table
    else:
        table.to_csv(f"stats/{filename}.csv")


table_absolute_change(filename="test_abs_change")

# Todo: check whether we want to include this big table
def linear_regressions_table(df, filename: str = None):
    # Initialization
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

    def variables_in_row(row):
        variables = []
        if "p_e" in row:
            variables.append("minority_competence")
        if "p_m" in row:
            variables.append("majority_competence")
        if "E" in row:
            variables.append("number_of_minority")
        if "I_e" in row:
            variables.append("influence_minority_proportion")
        if "h" in row:
            variables.append("homophily")
        return variables

    stats_results = pd.DataFrame(index=rows, columns=columns)

    # Analysis
    for row in rows:
        # construct multiple linear regression model
        variables = variables_in_row(row)

        Y = df[output]
        X = df[variables]
        X = sm.add_constant(X)
        model = sm.OLS(Y, X).fit()

        # R-value, model error and F-value
        Y_pred = model.predict(X)
        mean_square_error = np.square(np.subtract(Y, Y_pred)).mean()
        root_mean_square_error = math.sqrt(mean_square_error)
        stats_results.loc[row, "R_squared"] = round(model.rsquared, 3)
        stats_results.loc[row, "R_squared (adj)"] = round(model.rsquared_adj, 3)
        stats_results.loc[row, "root mean square error"] = round(
            root_mean_square_error, 3
        )
        stats_results.loc[row, "F value"] = round(model.fvalue)

        # standardized coefficients
        df_norm = pd.DataFrame(stats.zscore(df))
        Y_norm = df_norm[output]
        X_norm = df_norm[variables]
        X_norm = sm.add_constant(X_norm)
        model_norm = sm.OLS(Y_norm, X_norm).fit()

        #
        for variable in variables:
            column_p = f"{variable}_p_value"
            stats_results.loc[row, column_p] = round(model.pvalues[variable], 4)
            column_c = f"{variable}_coeff"
            stats_results.loc[row, column_c] = round(model.params[variable], 4)
            column_cstd = f"{variable}_coeff_std"
            stats_results.loc[row, column_cstd] = round(model_norm.params[variable], 4)
    if not filename:
        return stats_results
    else:
        print("yay")
        stats_results.to_csv(f"stats/{filename}.csv")


# linear_regressions_table(df=df, filename="test")

# Todo: create table with different datasets
# optional pruning of data
# data_low = data.loc[
#     (data["minority_competence"] > 0.55)
#     & (data["minority_competence"] < 0.60)
#     & (data["majority_competence"] > 0.55)
#     & (data["majority_competence"] < 0.60)
# ]
# data_med = data.loc[
#     (data["minority_competence"] > 0.60)
#     & (data["minority_competence"] < 0.65)
#     & (data["majority_competence"] > 0.60)
#     & (data["majority_competence"] < 0.65)
# ]
# data_high = data.loc[
#     (data["minority_competence"] > 0.65)
#     & (data["minority_competence"] < 0.70)
#     & (data["majority_competence"] > 0.65)
#     & (data["majority_competence"] < 0.70)
# ]

# Todo: remove if the rest works
def stats_analysis(dataframe: str = "full"):
    """Returns a pandas dataframe where each row represents one multiple linear regression.
    Columns with value 'NaN' where not used in the multiple linear regression.
    The first columns depict the p-value, the standardized coefficient of the associated independent variable, and
    how much the associated independent variable needs to unilaterally change to improve the collective accuracy by 5%.

    Standardized coefficients signify the mean change of the dependent variable given a one standard deviation
    shift in an independent variable.

    Parameters
    ==========
    dataset: str
        Type of dataset to analyse. Options: 'low', 'med', 'high', or 'full', default is 'full'
    columns: list
        List of all the independent variables
    output: str
        Dependent variable
    test: dict
        A dictionary with integer keys, where each value denotes one set of independent variables used for a regression

    Returns
    =======
    stats_results: pandas DataFrame
        An overview of the statistical analysis of the requested multiple linear regressions."""
    # Define dataset
    df = dataframe

    # Initialization
    columns = [
        "minority_competence",
        "majority_competence",
        "number_of_minority",
        "influence_minority_proportion",
        "homophily",
    ]
    output = "collective_accuracy"
    test: dict = {
        0: ["minority_competence", "majority_competence"],
        1: ["number_of_minority"],
        2: ["influence_minority_proportion"],
        3: ["influence_minority_proportion", "number_of_minority"],
        4: ["minority_competence", "majority_competence", "number_of_minority"],
        5: [
            "minority_competence",
            "majority_competence",
            "influence_minority_proportion",
        ],
        6: [
            "minority_competence",
            "majority_competence",
            "number_of_minority",
            "influence_minority_proportion",
        ],
        7: ["minority_competence", "majority_competence", "homophily"],
        8: [
            "minority_competence",
            "majority_competence",
            "homophily",
            "number_of_minority",
        ],
        9: [
            "minority_competence",
            "majority_competence",
            "homophily",
            "influence_minority_proportion",
        ],
        10: [
            "minority_competence",
            "majority_competence",
            "homophily",
            "number_of_minority",
            "influence_minority_proportion",
        ],
    }
    stats_results = pd.DataFrame(columns=columns)
    data_norm = pd.DataFrame(stats.zscore(df))

    # Analysis
    for v in range(len(test)):
        # construct multiple linear regression model
        variables = test[v]
        Y = df[output]
        X = df[variables]
        X = sm.add_constant(X)
        model = sm.OLS(Y, X).fit()

        # R-value, model error and F-value
        Y_pred = model.predict(X)
        mean_square_error = np.square(np.subtract(Y, Y_pred)).mean()
        root_mean_square_error = math.sqrt(mean_square_error)
        stats_results.loc[v, "R_squared"] = model.rsquared
        stats_results.loc[v, "R_squared (adj)"] = model.rsquared_adj
        stats_results.loc[v, "root mean square error"] = root_mean_square_error
        stats_results.loc[v, "F value"] = round(model.fvalue)

        # standardized coefficients
        Y_norm = data_norm[output]
        X_norm = data_norm[variables]
        X_norm = sm.add_constant(X_norm)
        model_norm = sm.OLS(Y_norm, X_norm).fit()

        #
        for x in variables:
            stats_results.loc[v, x] = (
                str(round(model.pvalues[x], 4))
                + " | "
                + str(round(model_norm.params[x], 4))
                + " | "
                + str(round(0.05 / model.params[x], 4))
            )
    return stats_results
