class Path:
    def __init__(self, lines):
        self.lines = lines
        self.__closest_to_origin(self.lines)
        self.current_line = self.lines[0]
        self.current_line.covered = True
        self.start_of_line = True
        self._followed_path = [self.current_line]

    def __closest_to_origin(self, lines):
        lines.sort(key=lambda l: l.distance_from_origin())

    def __find_closest_start(self, point):
        possible_lines = [line for line in self.lines if not line.covered]
        possible_lines.sort(key=lambda l: l.start.distance(
            self.current_line.get_start().x, self.current_line.get_start().y))
        return possible_lines.pop(0)

    def __find_closest_end(self, poit):
        possible_lines = [line for line in self.lines if not line.covered]
        possible_lines.sort(key=lambda l: l.end.distance(
            self.current_line.get_end().x, self.current_line.get_end().y))
        return possible_lines.pop(0)

    def __move_to_next_line(self):
        if self.start_of_line:
            next = self.__find_closest_start(self.current_line.start)
            next_coords = next.get_start_coords()
            x = next_coords["startX"]
            y = next_coords["startY"]
            self.current_line = next
            self.start_of_line = True
        else:
            next = self.__find_closest_end(self.current_line.end)
            next_coords = next.get_end_coords()
            x = next_coords["endX"]
            y = next_coords["endY"]
            self.current_line = next
            self.start_of_line = False
        self.current_line.cover()
        self._followed_path.append(self.current_line)

    def __move_to_end_point(self):
        if self.start_of_line:
            end_coords = self.current_line.get_end_coords()
            x = end_coords["endX"]
            y = end_coords["endY"]
            self.start_of_line = False
        else:
            start_coords = self.current_line.get_start_coords()
            x = start_coords["startX"]
            y = start_coords["startY"]
            self.start_of_line = True

    def go(self):
        self.__go(self.current_line)
        for line in self._followed_path:
            line.covered = False

    def __go(self, line):
        uncovered_lines = len([
            line for line in self.lines if not line.is_covered()])
        if uncovered_lines == 0:
            return True
        self.__move_to_end_point()
        self.__move_to_next_line()
        self.__go(self.current_line)

    def get_path(self):
        return self._followed_path
