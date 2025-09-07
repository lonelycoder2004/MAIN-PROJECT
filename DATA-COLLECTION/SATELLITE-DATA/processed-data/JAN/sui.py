import pandas as pd
import numpy as np

# Set your column names (update as needed)
col_names = ['date', 'time', 'latitude', 'longitude', 'WV_RADIANCE', 'VIS_ALBEDO', 'VIS_RADIANCE', 'TIR1_TEMP', 'TIR1_RADIANCE', 'TIR2_TEMP', 'TIR2_RADIANCE', 'MIR_RADIANCE', 'SWIR_RADIANCE', 'SAT_AZIMUTH', 'SAT_ELEVATION', 'SUN_AZIMUTH', 'SUN_ELEVATION']
df = pd.read_csv("Udyogamandal_Eloor.csv", names=col_names, header=None)

# Combine date and time into a datetime column
df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'], format='%d-%m-%Y %H:%M', errors='coerce')

# Convert all columns except date, time, datetime to numeric
for col in col_names[2:]:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Set hour for grouping
df['hour'] = df['datetime'].dt.floor('h')

# Group by hour and aggregate (mean for numeric columns)
agg_dict = {col: 'mean' for col in col_names[2:]}
result = df.groupby('hour').agg(agg_dict).reset_index()

# Reorder columns
ordered_cols = ['hour', 'latitude', 'longitude', 'WV_RADIANCE', 'VIS_ALBEDO', 'VIS_RADIANCE', 'TIR1_TEMP', 'TIR1_RADIANCE', 'TIR2_TEMP', 'TIR2_RADIANCE', 'MIR_RADIANCE', 'SWIR_RADIANCE', 'SAT_AZIMUTH', 'SAT_ELEVATION', 'SUN_AZIMUTH', 'SUN_ELEVATION']
result = result[ordered_cols]

# Save result
result.to_csv("hourly_Udyogamandal_Eloor.csv", index=False)
print("✅ Aggregation complete: Saved as hourly_Udyogamandal_Eloor.csv with updated headings")