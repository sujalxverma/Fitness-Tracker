import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from IPython.display import display
import matplotlib.animation as animation

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
mpl.style.use('seaborn-v0_8-deep')
mpl.rcParams['figure.figsize'] = (20, 5)
mpl.rcParams['figure.dpi'] = 100

# --------------------------------------------------------------
# Compare medium vs. heavy sets
# --------------------------------------------------------------
category_df = df.query("label == 'squat' and participant == 'A'").reset_index(drop=True)
fig , ax = plt.subplots()
category_df.groupby(["category"])["acc_y"].plot()
ax.set_ylabel("acc_y")
ax.set_xlabel("sample")
plt.legend()
# --------------------------------------------------------------

# --------------------------------------------------------------
# Plot multiple axis
# --------------------------------------------------------------
participant_df = df.query("label == 'bench'" ).sort_values("participant").reset_index(drop=True)
fig , ax = plt.subplots()
participant_df.groupby(["participant"])["acc_y"].plot()
ax.set_ylabel("acc_y")
ax.set_xlabel("sample")
plt.legend()

# --------------------------------------------------------------
# Create a loop to plot all combinations per sensor
# --------------------------------------------------------------


# --------------------------------------------------------------
# Combine plots in one figure
# --------------------------------------------------------------


# --------------------------------------------------------------
# Loop over all combinations and export for both sensors
# --------------------------------------------------------------