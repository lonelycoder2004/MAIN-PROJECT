import pandas as pd

# Read Excel file
df = pd.read_excel("MET+PM2.5.xlsx")

# Drop first 15 rows
df = df.iloc[15:]

# Save to CSV, writing None for missing values
df.to_csv("output.csv", index=False, na_rep="None")

# Reload CSV and skip first row (header info), use second row as header
# This will set the correct column names
skip_rows = 1  # skip the first row
header_row = 0  # use the second row as header

df_csv = pd.read_csv("output.csv", skiprows=skip_rows, header=header_row)

# Print actual column names to help you select the correct ones
print("Actual column names:", df_csv.columns.tolist())

# Select only the columns you want
selected_columns = ['From Date', 'PM2.5', 'RH', 'WS', 'WD', 'AT', 'RF', 'TOT-RF']
selected_df = df_csv[selected_columns]
selected_df.to_csv("output.csv", index=False, na_rep="None")
print("✅ Saved selected columns as output.csv")

print("✅ Conversion complete: Saved as output.csv and printed column names.")