import os
import rasterio
from rasterio.windows import from_bounds
import sys
from bounding_box import Mbr

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
    point = Point(input)
    import_raster(extent[0], extent[1], extent[2], extent[3])


if __name__ == '__main__':

    main()

