from common import Point
from region_indexer import Region
from collections import namedtuple

Borders = namedtuple('Borders', 'top, right, bottom, left')


class Regionv2(Region):
    @property
    def borders(self):
        return Borders(
            top=self.center.latitude+self.radius,
            right=self.center.longitude+self.radius,
            bottom=self.center.latitude-self.radius,
            left=self.center.longitude-self.radius
        )


class Part:
    """
    I am going to use a BST-like structures with one-dimensional parts
    of both latitude and longitude ordered in a specific way.
    """
    def __init__(self, left: int, right: int, region: Regionv2 or None):
        self.region = region
        self.left_node = None
        self.right_node = None

        self.left = left
        self.right = right

    @classmethod
    def search(cls, base_part: 'Part' or None, point_position: int, search_results=None):
        if base_part is None:
            return search_results

        if search_results is None:
            search_results = []

        if point_position < base_part.left:
            cls.search(base_part=base_part.left_node,
                       point_position=point_position,
                       search_results=search_results)
        else:
            if point_position in base_part:
                search_results.append(base_part.region)
            cls.search(base_part=base_part.right_node,
                       point_position=point_position,
                       search_results=search_results)

    def __contains__(self, point_position: int):
        return self.left <= point_position <= self.right


class Map:
    def __init__(self, board_size: int):
        self.board_size = board_size
        self.lat_root = Part(0, self.board_size, None)
        self.long_root = Part(0, self.board_size, None)

    def insert(self, region: Regionv2):
        lat_part = Part(
            left=region.borders.bottom,
            right=region.borders.top,
            region=region
        )
        long_part = Part(
            left=region.borders.left,
            right=region.borders.right,
            region=region
        )
        self._insert(self.lat_root, lat_part)
        self._insert(self.long_root, long_part)

    @classmethod
    def _insert(cls, base_part: 'Part' or None, other_part: 'Part'):
        if base_part.left > other_part.right:
            if base_part.left_node is None:
                base_part.left_node = other_part
            else:
                cls._insert(base_part=base_part.left_node,
                            other_part=other_part)
        else:
            if base_part.right_node is None:
                base_part.right_node = other_part
            else:
                cls._insert(base_part=base_part.right_node,
                            other_part=other_part)

    def batch_create(self, region_list):
        for raw_region in region_list:
            region = Regionv2(*raw_region)
            self.insert(region)

    def query(self, latitude, longitude):
        results_lat = Part.search(base_part=self.lat_root,
                                  point_position=latitude)
        results_long = Part.search(base_part=self.long_root,
                                   point_position=longitude)
        try:
            return list(set(results_lat).intersection(set(results_long)))
        except TypeError:
            return []
