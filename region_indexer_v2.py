from math import ceil
from common import Point


class SquareRegion:
    """
    Regions are divided as follows:
    #########
    # 3 # 0 #
    #########
    # 2 # 1 #
    #########
    """
    def __init__(self, parent: 'SquareRegion'=None,
                 subregion_number: int=None,
                 top: int=None,
                 right: int=None,
                 bottom: int=None,
                 left: int=None,
                 depth=None):
        if parent is None:
            self.parent = None
            self.top = top
            self.bottom = bottom
            self.left = left
            self.right = right
            self.remaining_depth = depth

        else:
            self.parent = parent
            self.remaining_depth = parent.remaining_depth-1
            self._update_coords(subregion_number)

        self.middle = Point(ceil((self.left + self.right) / 2),
                            ceil((self.top + self.bottom) / 2))

        if parent is not None:
            self._update_coords(subregion_number)

        if self.remaining_depth > 0:
            self.subregions = (SquareRegion(parent=self, subregion_number=index) for index in range(4))

    def _update_coords(self, subregion_number: int):
        if subregion_number in [0, 1]:
            self.left = ceil((self.parent.left + self.parent.right)/2)
            self.right = self.parent.right
        else:
            self.left = self.parent.left
            self.right = ceil((self.parent.left + self.parent.right)/2)

        if subregion_number in [2, 1]:
            self.top = self.parent.top
            self.bottom = ceil((self.parent.bottom + self.parent.top)/2)
        else:
            self.top = ceil((self.parent.top + self.parent.bottom)/2)
            self.bottom = self.parent.bottom


class RegionIndexerv2:
    def __init__(self, **kwargs):
        self.root = SquareRegion(**kwargs)

    def batch_create(self, region_list):
        for region in region_list:

