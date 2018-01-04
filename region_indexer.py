from common import Point


class Region:
    def __init__(self, latitude, longitude, radius, id_):
        self.center = Point(latitude, longitude)
        self.radius = radius
        self.id = id_

    def __contains__(self, point: 'Point') -> bool:
        return self.center.distance_to(point) <= self.radius

    def __repr__(self):
        return f'Region(id:{self.id}center:{self.center},radius:{self.radius})'


class RegionIndexer:
    def __init__(self):
        self.regions = []

    def batch_create(self, region_list):
        for region in region_list:
            self.regions.append(Region(*region))

    def query(self, latitude, longitude):
        return (region for region in self.regions if Point(latitude, longitude) in region)
