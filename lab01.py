import sys
from rtbot_blank import *
import logging
import time
import SocketServer
import socket
import threading
import Queue
import signal

FORMAT = '%(asctime)s %(levelname)s [%(filename)s:%(lineno)d] %(message)s'
DATE_FORMAT = '%H%M%S'
DEFAULT_VELOCITY = 100 # velocity in mm/s

	
def Turn(angle, dir):
	start = time.time()
	robot.Stop()
	robot.TurnInPlace(DEFAULT_VELOCITY, dir)
	time.sleep(8.3*angle/360)
	robot.Stop()
	return time.time() - start
	
def main():
	logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt=DATE_FORMAT) 
	global robot
	robot = Rtbot(sys.argv[1])
	robot.start()

	robot.DriveStraight(DEFAULT_VELOCITY)
	wallLastSeen = time.time()
	
	while True:
	
		#handle bumps
		bumpLeft = robot.sensors.GetLeftBump()
		bumpRight = robot.sensors.GetRightBump()
		
		if(bumpLeft + bumpRight >= 2):
			wallLastSeen += Turn(90, "ccw")
			robot.DriveStraight(DEFAULT_VELOCITY)
		elif(bumpLeft):
			wallLastSeen += Turn(1, "cw")
			robot.DriveStraight(DEFAULT_VELOCITY)
		elif(bumpRight):
			wallLastSeen += Turn(1, "ccw")
			robot.DriveStraight(DEFAULT_VELOCITY)
			
		#check if we can turn right
		if((time.time() - wallLastSeen) > 3):
			Turn(90, "cw")
			robot.DriveStraight(DEFAULT_VELOCITY)
			wallLastSeen = time.time()
		
		#update time since last saw right wall
		if(robot.sensors.GetWall() > 5):
			wallLastSeen = time.time()
			
if __name__ == '__main__':
  main()  
