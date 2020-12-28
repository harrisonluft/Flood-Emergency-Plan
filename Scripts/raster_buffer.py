import rasterio
from rasterio import mask
import geopandas as gpd
from fiona.crs import from_epsg


class RasterBuffer:

    def __init__(self, buffer, raster_path, out_path):
        self.buffer = buffer
        self.raster_path = raster_path
        self.out_path = out_path

# technique taken from https://automating-gis-processes.github.io/CSC/notebooks/L5/clipping-raster.html
    def clip_raster(self):
        self.geo = gpd.GeoDataFrame({'geometry': self.buffer}, index=[0], crs=from_epsg(27700))

        def getfeatures(gdf):
            """Static method to parse features from GeoDataFrame in such a manner that rasterio wants them"""
            import json
            return [json.loads(gdf.to_json())['features'][0]['geometry']]


        self.coords = getfeatures(self.geo)


        with rasterio.open(self.raster_path) as self.src:
            self.out_image, self.out_transform = rasterio.mask.mask(self.src, self.coords, crop=True)
            self.out_meta = self.src.meta

        self.out_meta.update({"driver": "GTiff",
                         "height": self.out_image.shape[1],
                         "width": self.out_image.shape[2],
                         "transform": self.out_transform})

        with rasterio.open(self.out_path, "w", **self.out_meta) as self.dest:
            self.dest.write(self.out_image)
