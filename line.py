import math


class Line:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.covered = False

    def get_start_coords(self):
        return {"startX": self.start.x, "startY": self.start.y}

    def get_end_coords(self):
        return {"endX": self.end.x, "endY": self.end.y}

    def line_distance(self):
        return math.sqrt((self.end.x - self.start.x)**2 + (self.end.y - self.start.y)**2)

    def distance_from_origin(self):
        return math.sqrt(self.start.x**2 + self.start.y**2)

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end

    def is_covered(self):
        return self.covered

    def cover(self):
        self.covered = True
