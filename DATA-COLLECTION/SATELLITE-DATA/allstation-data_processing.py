import math
import h5py
import os
import csv
import re

# Projection parameters (WGS84)
a = 6378137.0
b = 6356752.3142
lon0 = 75.0  # central meridian

x_ul = -6122571.993630046 # upper left x
y_ul = 6413524.594094472 # upper left y

dx = 3999.067272129357 # pixel size in x direction
dy = 3999.703519859353 # pixel size in y direction

nrows, ncols = 3207, 3062  # array shape

ee = math.sqrt(1 - (b**2 / a**2)) # eccentricity

def latandlong_to_pixels(lat, lon):
    phi = math.radians(lat)
    lam = math.radians(lon)
    lam0 = math.radians(lon0)
    x = a * (lam - lam0) # x coordinate in mercator projection
    y = a * math.log(
        math.tan(math.pi/4 + phi/2) *
        ((1 - ee * math.sin(phi)) / (1 + ee * math.sin(phi)))**(ee/2)
    ) # y coordinate in mercator projection
    col = (x - x_ul) / dx # column
    row = (y_ul - y) / dy # row
    return min(max(int(row), 0), nrows - 1), min(max(int(col), 0), ncols - 1)

def extract_datetime(fname):
    match = re.search(r'_(\d{2})([A-Z]{3})(\d{4})_(\d{2})(\d{2})_', fname)
    if match:
        day = match.group(1)
        month_str = match.group(2)
        year = match.group(3)
        hour = match.group(4)
        minute = match.group(5)
        months = {"JAN":"01", "FEB":"02", "MAR":"03", "APR":"04", "MAY":"05", "JUN":"06",
                  "JUL":"07", "AUG":"08", "SEP":"09", "OCT":"10", "NOV":"11", "DEC":"12"}
        month = months.get(month_str.upper(), "01")
        date_fmt = f"{day}-{month}-{year}"
        time_fmt = f"{hour}:{minute}"
        return date_fmt, time_fmt
    return "", ""

stations = [
    ("Plammoodu_Thiruvananthapuram", 8.5149093, 76.9435879),
    ("Kariavattom_Thiruvananthapuram", 8.563700, 76.886500),
    ("Polayathode_Kollam", 8.8787, 76.6073),
    ("Udyogamandal_Eloor", 10.073232, 76.302765),
    ("CorporationGround_Thrissur", 10.532400, 76.215900)
]

folder = "unprocessed-data/new_jan"

for station_name, lat, lon in stations:
    row, col = latandlong_to_pixels(lat, lon)
    output_csv = f"{station_name}newjannew.csv"
    with open(output_csv, "w", newline="") as csvfile:
        header = [
            "date", "time", "latitude", "longitude",
            "WV_RADIANCE",
            "VIS_ALBEDO", "VIS_RADIANCE",
            "TIR1_TEMP", "TIR1_RADIANCE",
            "TIR2_TEMP", "TIR2_RADIANCE",
            "MIR_RADIANCE",
            "SWIR_RADIANCE",
            "SAT_AZIMUTH",
            "SAT_ELEVATION",
            "SUN_AZIMUTH",
            "SUN_ELEVATION"
        ]
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for fname in os.listdir(folder):
            if fname.endswith(".h5"):
                file_path = os.path.join(folder, fname)
                try:
                    with h5py.File(file_path, "r") as f:
                        # WV
                        ds_wv = f["IMG_WV"]
                        dsr_wv = f["IMG_WV_RADIANCE"]
                        a_wv = ds_wv[0, row, col]
                        value_wv = dsr_wv[a_wv]

                        # VIS
                        ds_vis = f["IMG_VIS"]
                        dsr_vis_albedo = f["IMG_VIS_ALBEDO"]
                        dsr_vis_radiance = f["IMG_VIS_RADIANCE"]
                        a_vis = ds_vis[0, row, col]
                        value_vis_albedo = dsr_vis_albedo[a_vis]
                        value_vis_radiance = dsr_vis_radiance[a_vis]

                        # TIR1
                        ds_tir1 = f["IMG_TIR1"]
                        dsr_tir1_temp = f["IMG_TIR1_TEMP"]
                        dsr_tir1_radiance = f["IMG_TIR1_RADIANCE"]
                        a_tir1 = ds_tir1[0, row, col]
                        value_tir1_temp = dsr_tir1_temp[a_tir1]
                        value_tir1_radiance = dsr_tir1_radiance[a_tir1]

                        # TIR2
                        ds_tir2 = f["IMG_TIR2"]
                        dsr_tir2_temp = f["IMG_TIR2_TEMP"]
                        dsr_tir2_radiance = f["IMG_TIR2_RADIANCE"]
                        a_tir2 = ds_tir2[0, row, col]
                        value_tir2_temp = dsr_tir2_temp[a_tir2]
                        value_tir2_radiance = dsr_tir2_radiance[a_tir2]

                        # MIR
                        ds_mir = f["IMG_MIR"]
                        dsr_mir_radiance = f["IMG_MIR_RADIANCE"]
                        a_mir = ds_mir[0, row, col]
                        value_mir_radiance = dsr_mir_radiance[a_mir]

                        # SWIR
                        ds_swir = f["IMG_SWIR"]
                        dsr_swir_radiance = f["IMG_SWIR_RADIANCE"]
                        a_swir = ds_swir[0, row, col]
                        value_swir_radiance = dsr_swir_radiance[a_swir]
                        
                        #SAT_AZIMUTH
                        ds_sat_azimuth = f["Sat_Azimuth"]
                        value_sat_azimuth = ds_sat_azimuth[0, row, col]

                        #SAT_ELEVATION
                        ds_sat_elevation = f["Sat_Elevation"]
                        value_sat_elevation = ds_sat_elevation[0, row, col]

                        #SUN_AZIMUTH
                        ds_sun_azimuth = f["Sun_Azimuth"]
                        value_sun_azimuth = ds_sun_azimuth[0, row, col]

                        #SUN_ELEVATION
                        ds_sun_elevation = f["Sun_Elevation"]
                        value_sun_elevation = ds_sun_elevation[0, row, col]

                        date_str, time_str = extract_datetime(fname)
                        row_data = [
                            date_str, time_str, lat, lon,
                            value_wv,
                            value_vis_albedo, value_vis_radiance,
                            value_tir1_temp, value_tir1_radiance,
                            value_tir2_temp, value_tir2_radiance,
                            value_mir_radiance,
                            value_swir_radiance,
                            value_sat_azimuth,
                            value_sat_elevation,
                            value_sun_azimuth,
                            value_sun_elevation
                        ]
                        writer.writerow(row_data)
                except Exception as e:
                    print(f"Error processing {fname} for {station_name}: {e}")