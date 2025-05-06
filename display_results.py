import matplotlib.pyplot as plt
import pandas as pd
import os
import re

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

print(f"Discovered metrics: {metrics}")
print(f"Discovered models: {models}")
print(f"Discovered lambda values: {lambdas}")


# plot each model and metric for each test case, showing different lambdas
for metric in metrics:
    for test_case in test_cases:
        for lambda_val in lambdas:
            if lambda_val is None:
                continue  # Skip if no lambda value

            plt.figure(figsize=(10, 6))
            ax = plt.gca()

            for model in models:
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

            ax.set_xlabel("Load Percentage")
            ax.set_ylabel(metric)
            ax.set_title(f"{metric} for {test_case} with λ = {lambda_val} vs Load Percentage")
            ax.legend()
            ax.grid(True)
            plt.tight_layout()
            plt.show()

# Compare different models for each lambda value
for metric in metrics:
    for test_case in test_cases:
        for model in models:
            plt.figure(figsize=(10, 6))
            ax = plt.gca()

            for lambda_val in lambdas:
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
