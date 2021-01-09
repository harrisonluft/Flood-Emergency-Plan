import rasterio
from rasterio.merge import merge
import glob
import os

class MergeDEM:

    def __init__(self, raster_path, out_path):
        self.raster_path = raster_path
        self.out_path = out_path

    def merge_dems(self):
        # File and folder paths
        out_fp = os.path.join(self.out_path, "Elevation_Merge_Mosaic.tif")

        # Make a search criteria to select the DEM files
        search_criteria = "S*.asc"
        q = os.path.join(self.raster_path, search_criteria)

        # glob function can be used to list files from a directory with specific criteria
        dem_fps = glob.glob(q)
        # List for the source files
        src_files_to_mosaic = []
        # Iterate over raster files and add them to source -list in 'read mode'
        for fp in dem_fps:
            src = rasterio.open(fp)
            src_files_to_mosaic.append(src)

        # Merge function returns a single mosaic array and the transformation info
        mosaic, out_trans = merge(src_files_to_mosaic)

        # Copy the metadata
        out_meta = src.meta.copy()

        # Update the metadata
        out_meta.update({"driver": "GTiff",
                         "height": mosaic.shape[1],
                         "width": mosaic.shape[2],
                         "transform": out_trans,
                         }
                        )
        # Write the mosaic raster to disk
        with rasterio.open(out_fp, "w", **out_meta) as dest:
            dest.write(mosaic)

