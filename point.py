import math


class Point:
    def __init__(self, x, y, is_start=True, covered=False):
        self.x = x
        self.y = y
        self.is_start = is_start
        self.covered = covered

    def cover(self):
        self.covered = True

    def distance(self, x2, y2):
        return math.sqrt((x2 - self.x)**2 + (y2 - self.y)**2)
