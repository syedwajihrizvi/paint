import numpy as np
from math import sqrt, sin, pi

def movingAverage(data):
    window_size = 5
    i = 0
    moving_averages = [-1]*360
    slopeNew = [-1]*360
    f = open("average.txt", "w")
    while i < len(data) - window_size:
        if data[i] > 0 and data[i+window_size] > 0:
            window_average = round(np.sum(data[i:i+window_size])/window_size, 2)
            moving_averages[i+2] = window_average
            f.write(f"Index: {i}, Moving Average: {window_average} \n")
        i+=1
    f.close()
    minPoints = []
    counter = 0
    f = open("slope.txt", "w")
    for i in range(len(moving_averages) - 1):
        if moving_averages[i] > 0:
            new_slope = moving_averages[i+1] - moving_averages[i]
            f.write(f"{new_slope} \n")
            if abs(new_slope) < 0.05:
                minPoints.append([i,new_slope])
        else:
            f.write(f"-1000 \n")
    f.close()
    return minPoints

def find_angle_between_points(point_a, point_b):
    distance = sqrt((point_b.y-point_a.y)**2 + (point_b.x-point_a.x)**2)
    if point_a.x == point_b.x:
        return 90
    elif point_a.y == point_b.y:
        return 0
    else:
        diff_y = point_b.y - point_a.y
        return sin(diff_y/distance)*(180/pi)

    