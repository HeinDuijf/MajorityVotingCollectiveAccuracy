from stats.table_absolute_change import table_absolute_change
from stats.table_std_coefficients import table_std_coefficients
from stats.table_variance import table_variance
from stats.table_variance_multiple_datasets import table_variance_multiple_datasets

if __name__ == "__main__":
    data_file = "data/clean.csv"
    table_variance(data_file=data_file, output_file=f"table_variance")
    table_variance_multiple_datasets(
        data_file=data_file, output_file=f"table_variance_multiple"
    )
    table_std_coefficients(data_file=data_file, output_file=f"table_std_coeff")
    table_absolute_change(data_file=data_file, output_file=f"table_abs_change")
