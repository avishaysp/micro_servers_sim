import matplotlib.pyplot as plt
import pandas as pd

files_name = ["Avg. Processing Time",
              "Min. Processing Time",
              "Max. Processing Time",
              "STD. Processing Time",
              "Utilization Perc"]

fig = plt.figure(figsize=(15, 10))
gs = fig.add_gridspec(2, 3)

# Define subplot positions
ax1 = fig.add_subplot(gs[0, 0])  # First row, first column
ax2 = fig.add_subplot(gs[0, 1])  # First row, second column
ax3 = fig.add_subplot(gs[0, 2])  # Second row, first column
ax4 = fig.add_subplot(gs[1, 0])  # Second row, second column
ax5 = fig.add_subplot(gs[1, 1])  # Third row, spanning all columns

axes = [ax1, ax2, ax3, ax4, ax5]  # List of subplot axes

# Loop through each file and plot on the corresponding subplot
for i, file_name in enumerate(files_name):
    fn = f"results/{file_name}.csv"
    df = pd.read_csv(fn)

    df.rename(columns={df.columns[0]: "x"}, inplace=True)

    for column in df.columns[1:]:
        axes[i].plot(df["x"], df[column], marker='o', label=column)

    axes[i].set_xlabel("Load Percentage")
    axes[i].set_ylabel(file_name)
    axes[i].set_title(f"{file_name} VS Load Percentage")
    axes[i].legend()
    axes[i].grid(True)

# Adjust layout to prevent overlapping
plt.tight_layout()

# Show all subplots in the same figure
plt.show()
