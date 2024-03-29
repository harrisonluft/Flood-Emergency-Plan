import os
import sys
import rasterio
from shapely.geometry import Point
import numpy as np
from on_island import Contains
from raster_buffer import RasterBuffer
from nearest_itn import Itn
from ShortestPath import ShortestPath
from MapPlotting import MapPlotting
import geopandas as gpd


os.chdir('INSERT PATH HERE')
retval = os.getcwd()
print("Current working directory: %s" % retval)


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


def main():

    # import data
    input = user_input()

    user_gpd = {'geometry': [Point(input[0][0], input[0][1])]}
    gdf = gpd.GeoDataFrame(user_gpd, index=[0], crs='EPSG:27700')

    step_6 = Contains(gdf, os.path.join('Materials', 'shape', 'isle_of_wight.shp'))
    if step_6.is_within_geo():
        print('On to step 2')
    else:
        print('Not on the Isle of Wight - Stay where you are!')
        print('Closing application...')
        sys.exit(0)

    # import raster data
    user_point = Point(input[0][0], input[0][1])
    buffer = user_point.buffer(5000)

    # initialize Rasterbuffer(buffer, raster in path, clipped raster out path)
    step_2 = RasterBuffer(buffer, os.path.join('Materials', 'elevation', 'SZ.asc'),
                          os.path.join('Materials', 'elevation', '5k_mask.tif'))

    # clip raster to 5km circle
    step_2.clip_raster()

    # import 5km clipped raster
    clipped = rasterio.open(os.path.join('Materials', 'elevation', '5k_mask.tif'))

    # reading raster as numpy array
    matrix = clipped.read(1)

    # max height value
    max_height = np.amax(matrix)
    print('Max height from Numpy Array : ', max_height)

    #  index of max height
    result = np.where(matrix == np.amax(matrix))
    print('Max height index from Numpy Array:', result)

    #  coordinates of max height and geodataframe construction
    high_point = clipped.xy(result[0], result[1])
    high_point_obj = Point(float(high_point[0][0]), float(high_point[1][0]))
    if high_point_obj == user_point:
        print('You are already at the highest point! ')
        print('Closing application...')
        sys.exit(0)
    else:
        print('On to step 3')

    # Step 3 importing ITN network
    step_3 = Itn(os.path.join('Materials', 'itn', 'solent_itn.json'))

    # nearest nodes to both the user input and highest points
    step_3.itn_index()
    print('Nearest ITN node to user: ')
    step_3.nearest_node(user_point)
    print('Nearest ITN node to highest point:')
    step_3.nearest_node(high_point_obj)

    # step 4 shortest path with naismith's rules iterating through each link segment
    print('On to step 4')
    step_4 = ShortestPath(step_3.get_nearest_node(user_point)[0], step_3.get_nearest_node(high_point_obj)[0])
    step_4.get_itn_and_elevation()
    step_4.create_graph()
    shortest_path = step_4.get_shortest_path()[0]
    print('Shortest path: ' + str(shortest_path))

    print('On to step 5')
    step_5 = MapPlotting(shortest_path, user_point, high_point_obj)
    step_5.show_path()


if __name__ == '__main__':

    main()
