import rasterio
from rasterio import mask
from rasterio import plot
import os
from shapely.geometry import Point
import geopandas as gpd
from fiona.crs import from_epsg



path = os.chdir('C:\\Users\\17075\\Assignment_2')
print(path)

input = Point(450000, 85000)
buffer = input.buffer(5000)

# technique taken from https://automating-gis-processes.github.io/CSC/notebooks/L5/clipping-raster.html
geo = gpd.GeoDataFrame({'geometry': buffer}, index=[0], crs=from_epsg(27700))
print(geo)
print(geo.crs)

def getFeatures(gdf):
    """Function to parse features from GeoDataFrame in such a manner that rasterio wants them"""
    import json
    return [json.loads(gdf.to_json())['features'][0]['geometry']]


coords = getFeatures(geo)
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
rasterio.plot.show(clipped)