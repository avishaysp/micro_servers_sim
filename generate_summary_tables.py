import os
import pandas as pd


def load_csv_data(results_dir, metric_type, model_name, lambda_val, row_index=100):
    """Load data from a specific CSV file for the given model, metric and lambda value."""
    file_path = os.path.join(results_dir, f"{metric_type} - {model_name}_lambda_{lambda_val}.csv")
    try:
        df = pd.read_csv(file_path, index_col=0)
        if row_index in df.index:
            return df.loc[row_index].to_dict()
        else:
            print(f"Warning: Row {row_index} not found in {file_path}")
            return None
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None


def generate_summary_tables(results_dir, lambda_val=0.5, load_percentage=100):
    """Generate summary tables for all models at specified load percentage and lambda value."""
    # Define model names and test cases
    model_names = [
        "1) Monolithic",
        "2) 2 Services",
        "3) Logarithmic",
        "4) Distributed [RR]",
        "5) Distributed [LL]"
    ]

    test_cases = [
        "Constant Interval Tasks",
        "Random Interval Tasks",
        "Fragmented Tasks",
        "Overlapping Tasks",
        "Small Prob. of Failure"
    ]

    # Create DataFrames for utilization and average processing time
    util_df = pd.DataFrame(index=model_names, columns=test_cases)
    avg_time_df = pd.DataFrame(index=model_names, columns=test_cases)

    # Populate DataFrames
    for model_name in model_names:
        # Get utilization data
        util_data = load_csv_data(results_dir, "Utilization Perc", model_name, lambda_val, load_percentage)
        if util_data:
            for test_case in test_cases:
                if test_case in util_data:
                    util_df.loc[model_name, test_case] = util_data[test_case]

        # Get average processing time data
        avg_data = load_csv_data(results_dir, "Avg. Processing Time", model_name, lambda_val, load_percentage)
        if avg_data:
            for test_case in test_cases:
                if test_case in avg_data:
                    avg_time_df.loc[model_name, test_case] = avg_data[test_case]

    # Format utilization data as percentages
    util_df = util_df.astype(float).round(4)

    # Format avg processing time as integers (milliseconds)
    avg_time_df = avg_time_df.astype(float).round(0).astype(int)

    return util_df, avg_time_df


def save_tables_to_csv(util_df, avg_time_df, output_dir=None):
    """Save the generated tables to CSV files."""
    if output_dir is None:
        output_dir = os.getcwd()

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    util_path = os.path.join(output_dir, "utilization_summary_table.csv")
    avg_path = os.path.join(output_dir, "avg_processing_time_summary_table.csv")

    util_df.to_csv(util_path)
    avg_time_df.to_csv(avg_path)

    print(f"Saved utilization summary to: {util_path}")
    print(f"Saved average processing time summary to: {avg_path}")

    return util_path, avg_path


def print_tables(util_df, avg_time_df):
    """Print the tables in a formatted way."""
    print("\n\n=== UTILIZATION PERCENTAGE TABLE ===")
    print(util_df.to_string())

    print("\n\n=== AVERAGE PROCESSING TIME TABLE ===")
    print(avg_time_df.to_string())

    # Print in Markdown format for easy copy-pasting
    print("\n\n=== UTILIZATION PERCENTAGE TABLE (Markdown) ===")
    print(util_df.to_markdown())

    print("\n\n=== AVERAGE PROCESSING TIME TABLE (Markdown) ===")
    print(avg_time_df.to_markdown())


def main():
    # Path to results directory
    results_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tables")

    # Generate tables for lambda=0.5 and 100% load
    util_df, avg_time_df = generate_summary_tables(results_dir, lambda_val=0.5, load_percentage=100)

    # Print tables
    print_tables(util_df, avg_time_df)

    # Save tables to CSV
    save_tables_to_csv(util_df, avg_time_df, output_dir=output_dir)


if __name__ == "__main__":
    main()
