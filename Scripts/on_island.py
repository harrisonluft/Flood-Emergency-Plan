from shapely.geometry import MultiPolygon
import geopandas as gpd


class Contains:

    def __init__(self, user_gdf, shapefile_path):
        self.user_gdf = user_gdf
        self.shapefile_path = shapefile_path

    # solution adopted from https://geoffboeing.com/2016/10/r-tree-spatial-index-python/
    def is_within_geo(self):
        self.shapefile = gpd.read_file(self.shapefile_path)
        self.polygon = MultiPolygon(self.shapefile.geometry.iloc[0])
        self.gpd_point = self.user_gdf
        self.spatial_index = self.gpd_point.sindex
        possible_matches_index = list(self.spatial_index.intersection(self.polygon.bounds))
        possible_matches = self.gpd_point.iloc[possible_matches_index]
        precise_matches = possible_matches[possible_matches.intersects(self.polygon)]

        if precise_matches.empty:
            return False
        else:
            return True
