import xarray as xr

# Open GRIB file using cfgrib engine
ds = xr.open_dataset("data.grib", engine="cfgrib")

# Save as NetCDF
ds.to_netcdf("data.nc")
