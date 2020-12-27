import os
import rasterio
from rasterio import plot
from rasterio.windows import from_bounds
from shapely.geometry import Point
import numpy as np
from bounding_box import Mbr
from raster_buffer import RasterBuffer
import matplotlib.pyplot as plt
import geopandas as gpd

path = os.chdir('C:\\Users\\17075\\Assignment_2')

def user_input():
    data_list = []
    while True:
        try:
            user_point = input('Please input coordinate as Eastings, Northings: ')
            user_point_float = [float(user_point.split(',')[0]), float(user_point.split(',')[1])]
            break
        except:
            print('Invalid input, please try again')
    data_list.append(user_point_float)
    return data_list


#  from https://gis.stackexchange.com/questions/336874/
#  get-a-window-from-a-raster-in-rasterio-using-coordinates-instead-of-row-column-o

def import_raster(left, bottom, right, top):
    with rasterio.open(os.path.join('Materials', 'elevation', 'SZ.asc')) as sz:
        win = sz.read(1, window=from_bounds(left, bottom, right, top, sz.transform))
    return win


def main():

    # import data
    input = user_input()

    #  hardcode extent of bounding box
    extent = (430000, 80000, 465000, 95000)
    mbr = Mbr(extent)
    #  check if input point is within extent
    mbr.within_extent(input)

    # Verifying the bounding box works - test points are 1, 2 for fail
    # 450000, 85000 for pass
    print('On to step 2')

    # import raster data
    user_point = Point(input[0][0], input[0][1])
    buffer = user_point.buffer(5000)

    # initialize Rasterbuffer
    test = RasterBuffer(buffer,
                        os.path.join('Materials', 'elevation', 'SZ.asc'),
                        os.path.join('Materials', 'elevation', '5k_mask.tif'))

    test.clip_raster()

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

if __name__ == '__main__':

    main()

