import pandas as pd

# Load main dataset
main_df = pd.read_csv("output.csv")
main_df['From Date'] = pd.to_datetime(main_df['From Date'], format='%d-%m-%Y %H:%M', errors='coerce')

# Load BLH dataset
blh_df = pd.read_csv("BLH_Udyogamandal_Eloor.csv")
blh_df['time'] = pd.to_datetime(blh_df['time'], errors='coerce')

# Merge on standardized datetime
merged = pd.merge(main_df, blh_df[['time', 'blh']], left_on='From Date', right_on='time', how='inner')

# Select required columns
final_columns = ['From Date', 'PM2.5', 'RH', 'WS', 'WD', 'AT', 'RF', 'TOT-RF', 'blh']
final_df = merged[final_columns]

# Save result
final_df.to_csv("merged_output.csv", index=False, na_rep="None")
print("✅ Integration complete: Saved as merged_output.csv")