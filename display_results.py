import matplotlib.pyplot as plt
import pandas as pd
import os
import re
import argparse

# Set up argument parser
parser = argparse.ArgumentParser(description='Display simulation results with flexible filtering options.')
parser.add_argument('--metric', help='Specific metric to display (e.g., "Latency")')
parser.add_argument('--model', help='Specific model to display (e.g., "Monolith")')
parser.add_argument('--lambda', dest='lambda_val', type=float, help='Specific lambda value to display')
parser.add_argument('--test', help='Specific test case to display')
parser.add_argument('--plot-type', choices=['model', 'lambda', 'all'], default='all',
                    help='Type of plots to display: "model" (compare models), "lambda" (compare lambda values), or "all"')
parser.add_argument('--list', action='store_true', help='List all available metrics, models, lambdas, and test cases')
args = parser.parse_args()

results_dir = "results"
all_files = []
if os.path.exists(results_dir):
    all_files = [f for f in os.listdir(results_dir) if f.endswith(".csv")]
else:
    print(f"Error: Results directory '{results_dir}' not found.")
    exit()

if not all_files:
    print(f"Error: No CSV files found in '{results_dir}'.")
    exit()

metrics = set()
models = set()
lambdas = set()
test_cases = None
first_file_processed = False
file_pattern = re.compile(r"^(.*?) - (.*?)(?:_lambda_([\d.]+))?\.csv$")

for filename in all_files:
    match = file_pattern.match(filename)
    if match:
        # Extract metric, model name, and lambda
        groups = match.groups()
        metric = groups[0]
        model = groups[1]
        lambda_val = groups[2]
        
        metrics.add(metric)
        # For models, store just the base model name without lambda
        if lambda_val:
            models.add(model)
            lambdas.add(float(lambda_val))
        else:
            models.add(model)

        # Try to read test cases from the first valid file found
        if not first_file_processed:
            try:
                file_path = os.path.join(results_dir, filename)
                df_temp = pd.read_csv(file_path, index_col=0)
                # Assuming the first column is the index (load percentage)
                test_cases = df_temp.columns.tolist()
                first_file_processed = True
                print(f"Discovered test cases: {test_cases}")
            except Exception as e:
                print(f"Warning: Could not read {filename} to get test cases: {e}")
    else:
        print(f"Warning: Skipping file with unexpected name format: {filename}")

# Convert sets to sorted lists for consistent plotting order
metrics = sorted(list(metrics))
models = sorted(list(models))
lambdas = sorted(list(lambdas)) if lambdas else [None]

if not metrics:
    print("Error: No metrics found. Ensure filenames are in 'Metric Name - Model Name.csv' format.")
    exit()
if not models:
    print("Error: No models found. Ensure filenames are in 'Metric Name - Model Name.csv' format.")
    exit()
if not test_cases:
    print("Error: Could not determine test cases from any CSV file.")
    exit()

# If --list flag is set, display available options and exit
if args.list:
    print("\nAvailable options:")
    print(f"Metrics: {metrics}")
    print(f"Models: {models}")
    print(f"Lambda values: {lambdas}")
    print(f"Test cases: {test_cases}")
    exit()

# Filter based on args
selected_metrics = [args.metric] if args.metric and args.metric in metrics else metrics
selected_models = [args.model] if args.model and args.model in models else models
selected_lambdas = [args.lambda_val] if hasattr(args, 'lambda_val') and args.lambda_val in lambdas else lambdas
selected_tests = [args.test] if args.test and args.test in test_cases else test_cases

print("Plotting with filters:")
print(f"Metrics: {selected_metrics}")
print(f"Models: {selected_models}")
print(f"Lambda values: {selected_lambdas}")
print(f"Test cases: {selected_tests}")
print(f"Plot type: {args.plot_type}")


# plot comparison of different models with the same lambda value
def plot_models(results_dir, selected_metrics, selected_models, selected_lambdas, selected_tests):
    for metric in selected_metrics:
        for test_case in selected_tests:
            for lambda_val in selected_lambdas:
                if lambda_val is None:
                    continue  # Skip if no lambda value

                plt.figure(figsize=(10, 6))
                ax = plt.gca()

                for model in selected_models:
                    file_name = f"{metric} - {model}_lambda_{lambda_val}.csv"
                    file_path = os.path.join(results_dir, file_name)

                    if os.path.exists(file_path):
                        try:
                            df = pd.read_csv(file_path, index_col=0)
                            if test_case in df.columns:
                                x_values = df.index
                                ax.plot(x_values, df[test_case], marker='o', label=model)
                            else:
                                print(f"Warning: Test case '{test_case}' not found in {file_name}")
                        except Exception as e:
                            print(f"Error reading or plotting {file_path}: {e}")
                    else:
                        print(f"Warning: File not found: {file_name}")

                ax.set_xlabel("Load Percentage (%)")
                ax.set_ylabel(metric)
                ax.set_title(f"{metric} for {test_case} with λ = {lambda_val} vs Load Percentage")
                ax.legend()
                ax.grid(True)
                plt.tight_layout()
                plt.show()


# Compare different lambda values for each model
def plot_lamdas(results_dir, selected_metrics, selected_models, selected_lambdas, selected_tests):
    for metric in selected_metrics:
        for test_case in selected_tests:
            for model in selected_models:
                plt.figure(figsize=(10, 6))
                ax = plt.gca()

                for lambda_val in selected_lambdas:
                    if lambda_val is not None:
                        file_name = f"{metric} - {model}_lambda_{lambda_val}.csv"
                    else:
                        file_name = f"{metric} - {model}.csv"

                    file_path = os.path.join(results_dir, file_name)

                    if os.path.exists(file_path):
                        try:
                            df = pd.read_csv(file_path, index_col=0)
                            if test_case in df.columns:
                                x_values = df.index
                                label = f"λ = {lambda_val}" if lambda_val is not None else model
                                ax.plot(x_values, df[test_case], marker='o', label=label)
                            else:
                                print(f"Warning: Test case '{test_case}' not found in {file_name}")
                        except Exception as e:
                            print(f"Error reading or plotting {file_path}: {e}")
                    else:
                        print(f"Warning: File not found: {file_name}")

                ax.set_xlabel("Load Percentage")
                ax.set_ylabel(metric)
                ax.set_title(f"{metric} for {test_case} in {model} vs Load Percentage")
                ax.legend()
                ax.grid(True)
                plt.tight_layout()
                plt.show()


if args.plot_type in ['model', 'all']:
    plot_models(results_dir, selected_metrics, selected_models, selected_lambdas, selected_tests)


if args.plot_type in ['lambda', 'all']:
    plot_lamdas(results_dir, selected_metrics, selected_models, selected_lambdas, selected_tests)
