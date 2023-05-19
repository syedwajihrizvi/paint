import os
from math import cos, sin, pi, floor
from rplidar import RPLidar
from matplotlib import pyplot

PORT_NAME = '/dev/ttyUSB0'

lidar = RPLidar(PORT_NAME)

info = lidar.get_info()

# with open('lidar_info.txt', 'w') as f:
#     f.write(info)


health = lidar.get_health()
print(health)
# try:
#     for i, scan in enumerate(lidar.iter_scans()):
#         print(scan)
# except KeyboardInterrupt:
#     print("Stopping")
for i, scan in enumerate(lidar.iter_scans()):
    # print('%d: Got %d measurements' % (i,len(scan)))
    print(scan[1][1])
    #print(len(scan))
    # if i > 10:
    #     break

lidar.stop()
lidar.stop_motor()
lidar.disconnect()

