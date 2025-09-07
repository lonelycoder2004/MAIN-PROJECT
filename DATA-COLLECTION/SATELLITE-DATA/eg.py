import h5py

file_path = "data/JANUARY-2024/3RIMG_01JAN2024_0015_L1C_SGP_V01R00.h5"


with h5py.File(file_path, "r") as f:
    ds , dsr = f["IMG_WV"] , f["IMG_WV_RADIANCE"] # dataset
    a = ds[0,0,3061]
    print(a)
    