class Point:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def distance_to(self, other_point: 'Point'):
        x_dist = self.longitude - other_point.longitude
        y_dist = self.latitude - other_point.latitude

        return math.sqrt(x_dist**2 + y_dist**2)

    def __repr__(self):
        return f'Point({self.latitude}, {self.longitude})'
