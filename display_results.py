import matplotlib.pyplot as plt
import pandas as pd
import os
import re

# --- New code to discover metrics, models, and test cases ---
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
test_cases = None
first_file_processed = False
file_pattern = re.compile(r"^(.*?) - (.*?)\.csv$")

for filename in all_files:
    match = file_pattern.match(filename)
    if match:
        metric, model = match.groups()
        metrics.add(metric)
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

# --- New plotting logic ---
# Loop through each metric
for metric in metrics:
    # Loop through each test case
    for test_case in test_cases:
        plt.figure(figsize=(10, 6))  # Create a new figure for each metric/test_case pair
        ax = plt.gca()  # Get current axes

        # Loop through each model to plot its data on the current figure
        for model in models:
            file_name = f"{metric} - {model}.csv"
            file_path = os.path.join(results_dir, file_name)

            if os.path.exists(file_path):
                try:
                    df = pd.read_csv(file_path, index_col=0)
                    # Ensure the test case exists in this file's columns
                    if test_case in df.columns:
                         # Check if index is named, otherwise use df.index
                        if df.index.name:
                            x_values = df.index
                        else:
                             # If index has no name, assume it's the load percentage
                             # If read_csv didn't set index_col=0 correctly, this might need adjustment
                             x_values = df.index # Or potentially df.iloc[:, 0] if index is treated as data

                        ax.plot(x_values, df[test_case], marker='o', label=model)
                    else:
                        print(f"Warning: Test case '{test_case}' not found in {file_name}")
                except Exception as e:
                    print(f"Error reading or plotting {file_path}: {e}")
            else:
                print(f"Warning: File not found for model '{model}', metric '{metric}': {file_name}")

        ax.set_xlabel("Load Percentage")
        ax.set_ylabel(metric)
        ax.set_title(f"{metric} for {test_case} vs Load Percentage")
        ax.legend()
        ax.grid(True)
        plt.tight_layout()
        plt.show() # Show the plot for the current metric/test_case
