import pandas as pd
import statsmodels.api as sm
from scripts.basic_functions import convert_list_to_rows, convert_math_to_text


def table_variance_and_p(
    data_file: str = "data/clean.csv",
    output_file: str = None,
    independent_variables: list = None,
    dependent_variable: str = "collective_accuracy",
):
    # Initialize
    df = pd.read_csv(data_file)

    if independent_variables is None:
        independent_variables = [
            "number_of_minority",
            "homophily",
            "influence_minority_proportion",
            "minority_competence",
            "majority_competence",
        ]
    columns = [f"{dependent_variable} (R^2)"] + independent_variables
    rows: list = convert_list_to_rows(independent_variables)
    table = pd.DataFrame(index=rows, columns=columns)

    # Analysis
    for row in rows:
        # construct multiple linear regression model
        variables = convert_math_to_text(row, "list")
        Y = df[dependent_variable]
        X = df[variables]
        X = sm.add_constant(X)
        model = sm.OLS(Y, X).fit()

        # R-value
        Y_pred = model.predict(X)
        table.loc[row, f"{dependent_variable} (R^2)"] = round(model.rsquared, 3)

        # p-value
        for variable in variables:
            column_p = f"{variable}"
            table.loc[row, column_p] = round(model.pvalues[variable], 4)

    if not output_file:
        return table
    else:
        table.to_csv(f"{output_file}.csv")


if __name__ == "__main__":
    table_variance_and_p(
        data_file="../data/votes.csv",
        output_file="../stats/table_variance_votes",
        independent_variables=[
            "vote",
            "minority_competence",
            "majority_competence",
            "homophily",
            "influence_minority_proportion",
        ],
        dependent_variable="number_of_minority",
    )
    # table_variance_and_p(
    #     data_file="../data/clean.csv",
    #     output_file="../stats/table_variance_E",
    #     independent_variables=[
    #         "mean",
    #         "minority_competence",
    #         "majority_competence",
    #         "homophily",
    #         "influence_minority_proportion",
    #     ],
    #     dependent_variable="number_of_minority",
    # )
    # table_variance_and_p(
    #     data_file="../data/clean.csv",
    #     output_file="../stats/table_variance_mu",
    #     independent_variables=[
    #         "number_of_minority",
    #         "minority_competence",
    #         "majority_competence",
    #         "homophily",
    #         "influence_minority_proportion",
    #     ],
    #     dependent_variable="mean",
    # )
