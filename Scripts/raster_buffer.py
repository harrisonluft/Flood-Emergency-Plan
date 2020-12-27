import rasterio
from rasterio import mask
from rasterio import plot
import numpy as np
import os
from shapely.geometry import Point
import matplotlib.pyplot as plt
import geopandas as gpd
from fiona.crs import from_epsg


# input = Point(458967, 91676)
# buffer = input.buffer(5000)
class RasterBuffer:

    def __init__(self, buffer, raster_path, out_path):
        self.buffer = buffer
        self.raster_path = raster_path
        self.out_path = out_path

# technique taken from https://automating-gis-processes.github.io/CSC/notebooks/L5/clipping-raster.html
    def clip_raster(self):
        self.geo = gpd.GeoDataFrame({'geometry': self.buffer}, index=[0], crs=from_epsg(27700))

        def getfeatures(gdf):
            """Function to parse features from GeoDataFrame in such a manner that rasterio wants them"""
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

# clipped = rasterio.open(os.path.join('Materials', 'elevation', '5k_mask.tif'))
#
# #  reading raster as numpy array
# matrix = clipped.read(1)
#
# #  max height value
# maxHeight = np.amax(matrix)
# print('Max height from Numpy Array : ', maxHeight)
#
# #  index of max height
# result = np.where(matrix == np.amax(matrix))
# print('Returned tuple of arrays :', result)
#
# #  coordinates of max height and geodataframe construction
# high_point = clipped.xy(result[0], result[1])
# gdf = gpd.GeoDataFrame(geometry=gpd.points_from_xy(high_point[0], high_point[1]))
#
# #  Plotting taken from
# #  https://gis.stackexchange.com/questions/294072/how-can-i-superimpose-a-geopandas-dataframe-on-a-raster-plot
# fig, ax = plt.subplots()
# rasterio.plot.show(clipped, ax=ax)
# gdf.plot(ax=ax, color='red')
# plt.show()
