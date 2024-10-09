import json
import messaging
from time import time

class server(object):
    def __init__(self, ip,port,tasks):
        self.id = "sever"
        self.ip = ip
        self.port = port
        self.tasks = tasks
        self.robots ={}
    def writeLog(self,log):
        f = open("log.txt","a")
        f.write("\n")
        f.write(log)
        f.close()
    def saveJson(self):
        print(self.robots)
        temp = json.dumps(self.robots)
        print("Saving robot")
        f = open("robots.json", "w")
        f.write(temp)
        f.close()
        temp = {}
        for i in self.tasks:
            temp[i] = self.tasks[i].severInfoMessage()
        print(temp)
        temp = json.dumps(temp)
        print("Saving tasks")
        f = open("tasks.json", "w")
        f.write(temp)
        f.close()
        
    def loadRobotsJson(self):
        f = open("robots.json", "r")
        temp=f.read()
        f.close()   
        return json.loads(temp)   
    def checkTTL(self):
        for rid in self.robots:
            if self.robots[rid]["TTL"] != None and self.robots[rid]["TTL"]< (time()-150):
                self.robots[rid]["status"] = "Offline"
                tid = self.robots[rid]["task"]
                task = self.tasks[tid]
                task.deassignRobot(rid)
                self.writeLog("Robot id: "+rid+" non-responsive" )
    def setTTL(self, rid):
        self.robots[rid]["TTL"]=time()
        self.checkTTL()
    def readyUpRobot(self,rid,newtask):
       
        newtask.readyRobot(rid)
        
        if len(newtask.getReady())>=newtask.getrobotsRequired():
            for robot in newtask.getReady():
                self.writeLog(str("Sent: {} ".format(newtask.robotMessage())))
                messaging.send(self.robots[robot]["srcIP"],self.robots[robot]["srcPort"],newtask.robotMessage())
                self.setTTL(rid)
    def setTravel(self,rid,ip,port):
        newtask = self.tasks[self.robots[rid]["task"]]      
        if tuple(self.robots[rid]["location"]) != tuple(newtask.getLocation()):
            self.writeLog(str("Sent: Task:Travel,Location:{} ".format(newtask.getLocation())))
            messaging.send(ip,port,{"Task":"Travel","Location":newtask.getLocation()})
            self.setTTL(rid)
        else:
            self.readyUpRobot(rid,newtask)
            
    def setTask(self,ip,port,rid):
        if self.tasks != []:
            for tid in self.tasks:
                task = self.tasks[tid]
                if not task.completion():
                    if task.getrobotsRequired() > len(task.getAssigned()):
                        msg = {"Task":task.robotMessage()}
                        task.assignRobot(rid)
                        
                        self.robots[rid]["task"]=tid
                        self.setTravel(rid,ip,port)
                        break
                else:
                    continue
        else:
            msg = {"Task":None}
            self.writeLog("No more tasks")
            messaging.send(ip,port,msg)
    def run(self):
        while True: 
            msg =messaging.recive(self.ip,self.port)
            self.writeLog(str("recived: "+str(msg)))
            if msg["status"] == "idle":
                self.robots[msg["id"]]=msg
                self.setTask(msg["srcIP"],msg["srcPort"],msg["id"])
            if msg["status"] == "arrived":

                self.robots[msg["id"]]["location"] = msg["location"]
                self.robots[msg["id"]]["status"] = msg["status"]
                self.setTravel(msg["id"],msg["srcIP"],msg["srcPort"])
            
            self.saveJson()
            