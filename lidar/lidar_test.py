from lidar import Lidar

PORT_NAME = '/dev/ttyUSB0'
l = Lidar(PORT_NAME)
try:
    l.getData()

except KeyboardInterrupt:
    print('Stoping.')
    l.stop()
