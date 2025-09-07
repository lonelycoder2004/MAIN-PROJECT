import pandas as pd

# Load main dataset
main_df = pd.read_csv("merged_output.csv")
main_df['From Date'] = pd.to_datetime(main_df['From Date'], errors='coerce')

# Load hourly satellite dataset
hourly_df = pd.read_csv("hourly_Udyogamandal_Eloor.csv")
hourly_df['hour'] = pd.to_datetime(hourly_df['hour'], errors='coerce')

# Merge on datetime
merged = pd.merge(main_df, hourly_df, left_on='From Date', right_on='hour', how='inner')

# Remove rows with any None/NaN values
merged_clean = merged.dropna()
merged_clean = merged_clean.drop(columns=['hour','latitude','longitude'])

# Save result
merged_clean.to_csv("merged_final_no_none_final.csv", index=False, na_rep="None")

print("✅ Merge complete: Saved as merged_final_no_none.csv (rows with None/NaN removed)")