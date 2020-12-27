import sys

class Mbr:

    def __init__(self, extent):
        self.E1 = extent[0]
        self.N1 = extent[1]
        self.E2 = extent[2]
        self.N2 = extent[3]

    def within_extent(self, input):
        self.min_x = min(self.E1, self.E2)
        self.min_y = min(self.N1, self.N2)
        self.max_x = max(self.E1, self.E2)
        self.max_y = max(self.N1, self.N2)

        if (input[0][0] > self.max_x) or (input[0][1] > self.max_y) or \
            (input[0][0] < self.min_x) or (input[0][1] < self.min_y):

            print('Number provided is outside map extent')
            return sys.exit(0)
