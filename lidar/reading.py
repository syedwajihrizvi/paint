class Reading:

    def __init__(self, x_angle, y_angle, heading, x_dist, y_dist) -> None:
        self.x_angle = x_angle
        self.y_angle = y_angle
        self.heading = heading
        self.x_dist = x_dist 
        self.y_dist = y_dist
        
    def __eq__(self, other):
        return (self.x_angle == other.x_angle and \
        self.y_angle == other.y_angle and \
        self.heading == other.heading and \
        self.x_dist == other.x_dist and \
        self.y_dist == other.y_dist)
    
    @staticmethod
    def filter_readings(readings, radial_distance, max_angle_x, max_angle_y, max_heading):
        pass

