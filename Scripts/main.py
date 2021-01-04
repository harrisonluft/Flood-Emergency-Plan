import os
import rasterio
from rasterio import plot
from rasterio.windows import from_bounds
from shapely.geometry import Point
import numpy as np
from bounding_box import Mbr
from raster_buffer import RasterBuffer
from nearest_itn import Itn
from ShortestPath import ShortestPath
import matplotlib.pyplot as plt
import geopandas as gpd

#path = os.chdir('C:\\Users\\17075\\Assignment_2')
path = os.chdir('/Users/linchengze/PycharmProjects/Assignment_2')
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

    # hardcode extent of bounding box
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

    # initialize Rasterbuffer(buffer, raster in path, clipped raster out path)
    step_2 = RasterBuffer(buffer,
                        os.path.join('Materials', 'elevation', 'SZ.asc'),
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
    print(high_point_obj)
    gdf = gpd.GeoDataFrame(geometry=gpd.points_from_xy(high_point[0], high_point[1]))

    # Plotting taken from
    # https://gis.stackexchange.com/questions/294072/how-can-i-superimpose-a-geopandas-dataframe-on-a-raster-plot
    # fig, ax = plt.subplots()
    # rasterio.plot.show(clipped, ax=ax)
    # gdf.plot(ax=ax, color='red')
    # plt.show()

    # Step 3 importing ITN network
    print('On to step 3')

    step_3 = Itn(os.path.join('Materials', 'itn', 'solent_itn.json'))

    # nearest nodes to both the user input and highest points
    step_3.itn_index()
    step_3.nearest_node(user_point)
    step_3.nearest_node(high_point_obj)



    # step 4 shortest path with naismith's rules iterating through each link segment
    print('On to step 4')
    step_4 = ShortestPath(step_3.get_nearest_node(user_point)[0], step_3.get_nearest_node(high_point_obj)[0])
    step_4.get_itn_and_elevation()
    step_4.create_graph()
    shortest_path = step_4.get_shortest_path()[0]
    print('Shortest path: ' + str(shortest_path))

    print('On to step 5')



if __name__ == '__main__':

    main()
