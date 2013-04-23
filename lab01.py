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
	robot.TurnInPlace(DEFAULT_VELOCITY, dir)
	time.sleep(8.3*angle/360)
	robot.Stop()
	print "turned"

def moveBodyLength():
	robot.DriveStraight(DEFAULT_VELOCITY)
	start = time.time()
	while (time.time()-start < 3):
		if(robot.sensors.GetBump() == 1):
			onBump()
			return False
	robot.Stop()
	print "moved body length"
	return True

def DriveUntilWallDetected():
	robot.DriveStraight(DEFAULT_VELOCITY)

	while(robot.sensors.GetWall() == 0):
		pass

	robot.Stop()
	print "found wall"
	
def onBump():
	print "bumped"
	robot.Stop()
	Turn(90, "ccw")
	robot.DriveStraight(DEFAULT_VELOCITY)
	
def onLostWall():
	print "lost wall"
	if(moveBodyLength()):
		Turn(90, "cw")
		DriveUntilWallDetected()
	robot.DriveStraight(DEFAULT_VELOCITY)

def main():
	logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt=DATE_FORMAT) 
	global robot
	robot = Rtbot(sys.argv[1])
	robot.start()

	robot.DriveStraight(DEFAULT_VELOCITY)
		
	while True:
		if(robot.sensors.GetBump() == 1):
			onBump()
		if(robot.sensors.GetWall() == 0):
			onLostWall()
			
if __name__ == '__main__':
  main()  
