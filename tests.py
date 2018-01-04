import unittest

from time import time as timer
from statistics import mean

from region_indexer import Point, RegionIndexer, Region

TEST_SCALE = 200000


def measure_time(func, reps=1):
    scores = []
    for i in range(reps):
        start = timer()
        func()
        scores.append(timer()-start)
    return mean(scores)


class TestCodeEfficiency(unittest.TestCase):
    def setUp(self):
        self.test_data = [tuple([-i, i**2, i*2, f'#{i}']) for i in range(TEST_SCALE)]
        self.start = timer()
        self.indexer = RegionIndexer()

    def printTime(self, test_name, average=False):
        now = timer()
        print(f'\n{test_name} time: {(now - self.start):.10f} seconds.')
        if average:
            print(f'(average: {(now-self.start)/TEST_SCALE:.10f} seconds.)')

    def test_testing_module_efficiency(self):
        self.printTime('Test module setup')

    def test_setup_efficiency(self):
        self.indexer.batch_create(self.test_data)
        self.printTime('Full setup')

    def test_setup_with_filtering_efficiency(self):
        self.indexer.batch_create(self.test_data)
        points = (Point(i, i) for i in range(TEST_SCALE))

        for point in points:
            self.indexer.query(point.latitude, point.longitude)

        self.printTime(f'setup and filtering of {TEST_SCALE} queries',
                       average=True)


class TestCodeValidity(unittest.TestCase):
    def test_point_distance_is_measured_correctly(self):
        positions = [
            (1, 0),
            (-1, 0),
            (0, -1),
            (0, 1),
        ]

        base_point = Point(0, 0)

        for position in positions:
            self.assertEqual(base_point.distance_to(Point(*position)), 1)

    def test_point_found_in_region(self):
        region = Region(0, 0, 1, "#center")

        positions_in_region = [
            (0, 0),
            (0, 1),
            (1, 0),
            (-1, 0),
            (-0.5, 0),
            (0, 0.99),
        ]

        positions_not_in_region = [
            (1, 1),
            (100, 100),
            (-100, -100),
            (-1, -1),
        ]

        for position in positions_in_region:
            self.assertIn(Point(*position), region)

        for position in positions_not_in_region:
            self.assertNotIn(Point(*position), region)

if __name__ == '__main__':
    unittest.main()
