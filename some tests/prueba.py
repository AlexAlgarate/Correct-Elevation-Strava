import pandas as pd

df = pd.read_csv("summary_elev_0.csv")
print(df.columns)

print(df["sport_type"].unique())

id_virtual_rides = df.loc[df['sport_type'] == 'VirtualRide']
# print(id_virtual_rides[["total_elevation_gain", "id", "name"]])
df["sport_type"].replace({"VirtualRide": "Ride"}, inplace=True)

# print(df.loc[df["total_elevation_gain"] == 0]["sport_type"].unique())
# print(
#     df.loc[
#         (df["total_elevation_gain"] == 0)
#         &
#         (df["sport_type"] == "VirtualRide")
#     ]
# )
cycling_activities_zero_elevation = df.loc[
    (df["sport_type"] == "Ride") & (df["total_elevation_gain"] == 0)
][["name", "id", "distance", "moving_time"]]
print(cycling_activities_zero_elevation)

# df.loc to txt file
with open("cycling_activities_to_correct.txt", "w", encoding="utf-8") as act:
    text = cycling_activities_zero_elevation.to_string(
        header=False,
        index=False
    )
    act.write(text)

    # def get_ids_to_correct(self, df):
    #     ids_to_correct_elevation = df.loc[
    #         (df['sport_type'].isin(['Ride', 'Run']))
    #         &
    #         (df['total_elevation_gain'] == 0)
    #     ]['id'].to_list()
    #     return ids_to_correct_elevation
