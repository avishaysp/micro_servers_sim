import matplotlib.pyplot as plt
import pandas as pd

files_name = ["Avg. Processing Time",
              "Min. Processing Time",
              "Max. Processing Time",
              "Var. Processing Time",
              "Utilization Perc"]

for file_name in files_name:
    fn = f"results/{file_name}.csv"
    df = pd.read_csv(fn)

    df.rename(columns={df.columns[0]: "x"}, inplace=True)

    plt.figure(figsize=(10, 6))
    for column in df.columns[1:]:
        plt.plot(df["x"], df[column], marker='o', label=column)

    plt.xlabel("Load Percentage")
    plt.ylabel(file_name)
    plt.title(f"{file_name} VS Load Percentage")
    plt.legend()
    plt.grid(True)

    plt.show()