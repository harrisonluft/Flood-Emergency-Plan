import os
from bounding_box import MBR

cwd = os.getcwd()
print(cwd)
path = os.path.dirname(cwd)
print(path)


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

    #  hardcode extent of bounding box
    extent = (430000, 80000, 465000, 95000)
    mbr = MBR(extent)
    mbr.within_extent(input)

    # Verifying the bounding box works - test points are 1, 2 for fail
    # 450000, 85000 for pass
    print('On to step 2')



if __name__ == '__main__':

    main()

