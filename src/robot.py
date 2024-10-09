import messaging
from time import sleep
from math import sqrt
import sys
# example start command 
#python3 robot.py 1 localhost 5006 localhost 5005 0 0
class Robot(object):
    def __init__(self, id, ip,port,severip,severport,location):
        self.id = id
        self.ip = ip
        self.port= port
        self.severip = severip
        self.severport = severport
        self.location = location
        self.currentTask = None
        self.currentOperation = "idle"

    def sendStatus(self,status):
        msg = {"location":self.location,"srcIP":self.ip,"srcPort":self.port,"status":status,"id":self.id}
        
        messaging.send(self.severip,self.severport,msg)
        msg = messaging.recive(self.ip,self.port)
        if msg["Task"] == None:
            return
        else:
            self.currentTask = msg
            self.currentOperation = "start"
    def running(self):
        
        while True:
            
            print(self.currentOperation)
            if self.currentOperation == "idle" or self.currentOperation == "arrived":
              #  try:
                self.sendStatus(self.currentOperation)
                """except:
                    print("Error")"""
            elif self.currentTask != "None":
                tlocation = self.currentTask["Location"]
                if tlocation != self.location:
                    distance =  sqrt(((self.location[0]-tlocation[0])**2)+((self.location[1]-tlocation[1])**2))
                    print("sleeping for",distance*10)
                    sleep(distance*10)
                    self.location = tlocation
                    self.currentOperation = "arrived"
                else:
                    self.currentOperationr = "working"
                    sleep(self.currentTask["Time"]*10)
                    self.currentOperation ="idle"

if __name__ == '__main__':
    r = Robot(sys.argv[1],sys.argv[2],int(sys.argv[3]),sys.argv[4],int(sys.argv[5]),(int(sys.argv[6]),int(sys.argv[7])))
    r.running()