import rasterio
from rasterio import mask
from rasterio import plot
import numpy as np
import os
from shapely.geometry import Point
import matplotlib.pyplot as plt
import geopandas as gpd
from fiona.crs import from_epsg

path = os.chdir('C:\\Users\\17075\\Assignment_2')

input = Point(458967, 91676)
buffer = input.buffer(5000)

# technique taken from https://automating-gis-processes.github.io/CSC/notebooks/L5/clipping-raster.html
geo = gpd.GeoDataFrame({'geometry': buffer}, index=[0], crs=from_epsg(27700))
print(geo)
print(geo.crs)


def getfeatures(gdf):
    """Function to parse features from GeoDataFrame in such a manner that rasterio wants them"""
    import json
    return [json.loads(gdf.to_json())['features'][0]['geometry']]


coords = getfeatures(geo)
print(coords)

with rasterio.open(os.path.join('Materials', 'elevation', 'SZ.asc')) as src:
    out_image, out_transform = rasterio.mask.mask(src, coords, crop=True)
    out_meta = src.meta

out_meta.update({"driver": "GTiff",
                 "height": out_image.shape[1],
                 "width": out_image.shape[2],
                 "transform": out_transform})

with rasterio.open(os.path.join('Materials', 'elevation', '5k_mask.tif'), "w", **out_meta) as dest:
    dest.write(out_image)

clipped = rasterio.open(os.path.join('Materials', 'elevation', '5k_mask.tif'))

#  reading raster as numpy array
matrix = clipped.read(1)

#  max height value
maxHeight = np.amax(matrix)
print('Max height from Numpy Array : ', maxHeight)

#  index of max height
result = np.where(matrix == np.amax(matrix))
print('Returned tuple of arrays :', result)

#  coordinates of max height and geodataframe construction
high_point = clipped.xy(result[0], result[1])
gdf = gpd.GeoDataFrame(geometry=gpd.points_from_xy(high_point[0], high_point[1]))

#  Plotting taken from
#  https://gis.stackexchange.com/questions/294072/how-can-i-superimpose-a-geopandas-dataframe-on-a-raster-plot
fig, ax = plt.subplots()
rasterio.plot.show(clipped, ax=ax)
gdf.plot(ax=ax, color='red')
plt.show()
