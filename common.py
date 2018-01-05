from geopy.distance import vincenty
import math


class Point:
    """
    Good old point
    """
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def distance_to(self, other_point: 'Point'):
        """
        :param other_point:
        :return: distance between the two
        """
        x_dist = self.longitude - other_point.longitude
        y_dist = self.latitude - other_point.latitude

        return math.sqrt(x_dist**2 + y_dist**2)

    def __repr__(self):
        return f'Point({self.latitude}, {self.longitude})'


class Point2:
    """
    I decided to treat Earth as it was flat to silmplify my calculations. This class could be a starter
    for thinking of it as a spheroid, which we all know it is not. It IS flat, google it.
    """
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def distance_to(self, other_point: 'Point'):
        """
        :param other_point:
        :return: distance to other point taking Earth's official shape into consideration.
        """
        return vincenty((self.latitude, self.longitude), (other_point.latitude, other_point.longitude)).km

    def __repr__(self):
        return f'Point({self.latitude}, {self.longitude})'
