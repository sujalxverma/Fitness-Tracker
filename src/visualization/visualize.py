import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from IPython.display import display

# --------------------------------------------------------------
# Load data
# --------------------------------------------------------------
df = pd.read_pickle("../../data/interim/01_data_processed.pkl")
df

# --------------------------------------------------------------
# Plot single columns
# --------------------------------------------------------------
set_df = df[df["set"]==1]
plt.plot(set_df["acc_y"], label="acc_y")
plt.plot(set_df["acc_y"].reset_index(drop=True), label="acc_y")


# --------------------------------------------------------------
# Plot all exercises
# --------------------------------------------------------------
for label in df['label'].unique():
    label_df = df[df['label'] == label]
    #display(label_df.head())   # display the data frame in for loop
    # fig, ax = plt.subplots(figsize=(10, 6))
    plt.figure(figsize=(10, 6))
    plt.plot(label_df[:100]["acc_y"].reset_index(drop=True), label=label)
    plt.legend()

# --------------------------------------------------------------
# Adjust plot settings
# --------------------------------------------------------------


# --------------------------------------------------------------
# Compare medium vs. heavy sets
# --------------------------------------------------------------


# --------------------------------------------------------------
# Compare participants
# --------------------------------------------------------------


# --------------------------------------------------------------
# Plot multiple axis
# --------------------------------------------------------------


# --------------------------------------------------------------
# Create a loop to plot all combinations per sensor
# --------------------------------------------------------------


# --------------------------------------------------------------
# Combine plots in one figure
# --------------------------------------------------------------


# --------------------------------------------------------------
# Loop over all combinations and export for both sensors
# --------------------------------------------------------------