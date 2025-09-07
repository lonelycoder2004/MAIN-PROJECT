import xarray as xr
import pandas as pd

# Open dataset
ds = xr.open_dataset("data.nc")

# Keep only BLH
blh = ds["blh"]

# Define stations with lat/lon
stations = [
    ("Plammoodu_Thiruvananthapuram", 8.5149093, 76.9435879),
    ("Kariavattom_Thiruvananthapuram", 8.563700, 76.886500),
    ("Polayathode_Kollam", 8.8787, 76.6073),
    ("Udyogamandal_Eloor", 10.073232, 76.302765),
    ("CorporationGround_Thrissur", 10.532400, 76.215900),
]

# Extract BLH for each station and save separately
for name, lat, lon in stations:
    # Select nearest grid point
    station_blh = blh.sel(latitude=lat, longitude=lon, method="nearest")
    df_station = station_blh.to_dataframe().reset_index()
    df_station["Station"] = name

    # Save each station's BLH as a separate CSV
    filename = f"BLH_{name}.csv"
    df_station.to_csv(filename, index=False)
    print(f"✅ Saved {filename}")
