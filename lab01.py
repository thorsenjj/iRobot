import sys
from rtbot_blank import *
import logging
import time
import SocketServer
import socket
import threading
import Queue
import signal
import time
import math

FORMAT = '%(asctime)s %(levelname)s [%(filename)s:%(lineno)d] %(message)s'
DATE_FORMAT = '%H%M%S'


def RoundCorner():
	robot.Drive(100, -200)
	time.sleep(2.85)
	robot.Stop()
	
def Turn(angle, dir):
	robot.TurnInPlace(100, dir)
	time.sleep(8.5*angle/360)
	robot.Stop()

def main():
	logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt=DATE_FORMAT) 
	global robot
	robot = Rtbot(sys.argv[1])
	robot.start()
	
	while True:
		robot.DriveStraight(100)
		if(robot.sensors.GetBump() == 1):
			robot.Stop()
			Turn(90, "ccw")
		if(robot.sensors.GetWall() == 0):
			robot.Stop()
			RoundCorner()
	
  

if __name__ == '__main__':
  main()  
