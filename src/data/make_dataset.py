import pandas as pd
from glob import glob

# --------------------------------------------------------------
# Read single CSV file
# --------------------------------------------------------------
# single_file_acc = pd.read_csv(
#     "../../data/raw/MetaMotion/A-bench-heavy2-rpe8_MetaWear_2019-01-11T16.10.08.270_C42732BE255C_Accelerometer_12.500Hz_1.4.4.csv"
# )
# single_file_gyr = pd.read_csv(
#     "../../data/raw/MetaMotion/A-bench-heavy2-rpe8_MetaWear_2019-01-11T16.10.08.270_C42732BE255C_Gyroscope_25.000Hz_1.4.4.csv"
# )

# --------------------------------------------------------------
# List all data in data/raw/MetaMotion
# --------------------------------------------------------------

# files = glob("../../data/raw/MetaMotion/*.csv")
# files[0]

# --------------------------------------------------------------
# Extract features from filename
# --------------------------------------------------------------
# data_path = "../../data/raw/MetaMotion/"
# f = files[0]
# participant = f.split("-")[0].replace(data_path, "")
# label = f.split("-")[1]
# category = f.split("-")[2].rstrip("123").rstrip("_MetaWear_2019")
# # print(participant , label , category)

# df = pd.read_csv(f)
# df["participant"] = participant
# df["label"] = label
# df["category"] = category
# df

# --------------------------------------------------------------
# Read all files
# --------------------------------------------------------------
# acc_df = pd.DataFrame()
# gyr_df = pd.DataFrame()
# acc = "Accelerometer"
# gyr = "Gyroscope"
# acc_set = 1
# gyr_set = 1
# for f in files:
#     paticpant = f.split("-")[0].replace(data_path, "")
#     label = f.split("-")[1]
#     category = f.split("-")[2].rstrip("123").rstrip("_MetaWear_2019")
#     df = pd.read_csv(f)
#     df["participant"] = participant
#     df["label"] = label
#     df["category"] = category

#     if acc in f:
#         df["set"] = acc_set
#         acc_set += 1
#         acc_df = pd.concat([acc_df, df])
#     if gyr in f:
#         df["set"] = gyr_set
#         gyr_set += 1
#         gyr_df = pd.concat([gyr_df, df])


# --------------------------------------------------------------
# Working with datetimes
# --------------------------------------------------------------

# pd.to_datetime(df["epoch (ms)"] , unit="ms")
# acc_df.index = pd.to_datetime(acc_df["epoch (ms)"], unit="ms")
# gyr_df.index = pd.to_datetime(gyr_df["epoch (ms)"], unit="ms")

# acc_df.drop(columns=["epoch (ms)", "time (01:00)", "elapsed (s)"], inplace=True)
# gyr_df.drop(columns=["epoch (ms)", "time (01:00)", "elapsed (s)"], inplace=True)


# --------------------------------------------------------------
# Turn into function
# --------------------------------------------------------------

files = glob("../../data/raw/MetaMotion/*.csv")
data_path = "../../data/raw/MetaMotion/"


def read_data_from_files(files):
    acc_df = pd.DataFrame()
    gyr_df = pd.DataFrame()
    acc = "Accelerometer"
    gyr = "Gyroscope"
    acc_set = 1
    gyr_set = 1
    for f in files:
        participant = f.split("-")[0].replace(data_path, "")
        label = f.split("-")[1]
        category = f.split("-")[2].rstrip("123").rstrip("_MetaWear_2019")
        df = pd.read_csv(f)
        df["participant"] = participant
        df["label"] = label
        df["category"] = category

        if acc in f:
            df["set"] = acc_set
            acc_set += 1
            acc_df = pd.concat([acc_df, df])
        if gyr in f:
            df["set"] = gyr_set
            gyr_set += 1
            gyr_df = pd.concat([gyr_df, df])
    acc_df.index = pd.to_datetime(acc_df["epoch (ms)"], unit="ms")
    gyr_df.index = pd.to_datetime(gyr_df["epoch (ms)"], unit="ms")

    acc_df.drop(columns=["epoch (ms)", "time (01:00)", "elapsed (s)"], inplace=True)
    gyr_df.drop(columns=["epoch (ms)", "time (01:00)", "elapsed (s)"], inplace=True)

    return acc_df, gyr_df


acc_df, gyr_df = read_data_from_files(files)


# --------------------------------------------------------------
# Merging datasets
# --------------------------------------------------------------

data_merged = pd.concat([acc_df.iloc[:, :3], gyr_df], axis=1)
# first few colums of acc_df then columns of gyr_df
# data_merged.dropna()
data_merged.columns = [
    "acc_x",
    "acc_y",
    "acc_z",
    "gyr_x",
    "gyr_y",
    "gyr_z",
    "participant",
    "label",
    "category",
    "set",
]
data_merged


# --------------------------------------------------------------
# Resample data (frequency conversion)
# --------------------------------------------------------------

# Accelerometer:    12.500HZ
# Gyroscope:        25.000Hz    ->  means, more data is recorded due to higher frequency.

sampling = {
    "acc_x": "mean",
    "acc_y": "mean",
    "acc_z": "mean",
    "gyr_x": "mean",
    "gyr_y": "mean",
    "gyr_z": "mean",
    "participant": "last",
    "label": "last",
    "category": "last",
    "set": "last",
}

data_merged
data_merged[:1000].resample(rule="200ms").apply(sampling)

# split by day
days = [g for n, g in data_merged.groupby(pd.Grouper(freq="D"))]
data_resampled = pd.concat(
    [df.resample(rule="200ms").apply(sampling).dropna() for df in days]
)

data_resampled.info()
data_resampled["set"] = data_resampled["set"].astype(int)
data_resampled.info()
# --------------------------------------------------------------
# Export dataset
# --------------------------------------------------------------

data_resampled.to_pickle("../../data/interim/01_data_processed.pkl")
