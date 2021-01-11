import os
import json
import rasterio
from rasterio import plot
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from cartopy import crs
from shapely.geometry import LineString
from shapely.geometry import Polygon
import networkx as nx
import numpy
from matplotlib_scalebar.scalebar import ScaleBar

class MapPlotting:

    def __init__(self, path, user_point, highest_point):
        self.path = path
        self.user_point = user_point
        self.highest_point = highest_point

    def show_path(self):
        #convert shortest path to geodataframe
        #refenrence: https://github.com/aldolipani/CEGE0096/blob/master/8%20-%20Week/8%20-%20RTree%20and%20NetworkX%20with%20Solutions.ipynb
        itn_json = os.path.join('Materials', 'itn', 'solent_itn.json')
        with open(itn_json, 'r') as f:
            itn = json.load(f)
        road_links = itn['roadlinks']

        g = nx.Graph()
        for link in road_links:
            g.add_edge(road_links[link]['start'], road_links[link]['end'], fid=link, weight=road_links[link]['length'])

        links = []
        geom = []

        first_node = self.path[0]
        for node in self.path[1:]:
            link_fid = g.edges[first_node, node]['fid']
            links.append(link_fid)
            geom.append(LineString(road_links[link_fid]['coords']))
            first_node = node

        shortest_path_gpd = gpd.GeoDataFrame({'fid': links, 'geometry': geom})


        #add background
        wight_background = os.path.join('Materials', 'background', 'raster-50k_2724246.tif')
        background = rasterio.open(wight_background)
        back_array = background.read(1)
        palette = np.array([value for key, value in background.colormap(1).items()])
        background_image = palette[back_array]
        bounds = background.bounds
        extent = [bounds.left, bounds.right, bounds.bottom, bounds.top]
        display_extent = [bounds.left, bounds.right, bounds.bottom, bounds.top]

        fig = plt.figure(figsize=(3, 3), dpi=300)
        ax = fig.add_subplot(1, 1, 1, projection=crs.OSGB())

        ax.imshow(background_image, origin='upper', extent=extent, zorder=0)

        shortest_path_gpd.plot(ax=ax, edgecolor='blue', linewidth=0.5, zorder=2)

        ax.set_extent(display_extent, crs=crs.OSGB())

        # add north arrow
        x = 0.95
        y = 0.95
        north_arrow_length = 0.18
        ax.annotate('N', xy=(x, y), xytext=(x, y - north_arrow_length),
                    xycoords='axes fraction',
                    horizontalalignment='center',
                    verticalalignment='center',
                    fontsize=8,
                    arrowprops=dict(arrowstyle='-|>', facecolor='black'))

        # add scale bar
        scale_bar = ScaleBar(dx=1, units='m', scale_loc='bottom',
                             location='lower left', frameon=False,
                             border_pad=1, sep=3, rotation="horizontal")
        ax.add_artist(scale_bar)

        ax.scatter(self.user_point.x, self.user_point.y, marker = '.', c='pink', zorder=3, label='User Point', )
        ax.scatter(self.highest_point.x, self.highest_point.y, marker = '.', c='brown', zorder=3, label='Highest Point')
        ax.legend(loc='lower right', prop={'size': 5})


        # 5km buffer (transparent elavation raster)
        buffer_5km = self.user_point.buffer(5000)
        elevation = rasterio.open(os.path.join('Materials','elevation','SZ.asc'))
        elevation_boundary = elevation.bounds
        elevation_polygon = Polygon([(elevation_boundary[0], elevation_boundary[1]),
                                     (elevation_boundary[2], elevation_boundary[1]),
                                     (elevation_boundary[2], elevation_boundary[3]),
                                     (elevation_boundary[0], elevation_boundary[3])])
        intersection = buffer_5km.intersection(elevation_polygon)
        if intersection.area != 0:
            clipped_elevation, trans = rasterio.mask.mask(elevation, [intersection], crop=True, filled=False)
        rasterio.plot.show(source=clipped_elevation, transform=trans,
                           origin="upper", alpha=0.5,
                           ax=ax, zorder=1, cmap='terrain')
        norm = cm.colors.Normalize(vmax=numpy.max(clipped_elevation),
                                   vmin=numpy.min(clipped_elevation))
        colourmap = plt.cm.ScalarMappable(norm=norm, cmap='terrain')

        #add colorbar for elevation
        plt.colorbar(colourmap, label='Elevation within 5km (m)')



        plt.show()

