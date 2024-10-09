class task(object):
    def __init__(self,id,location,time,task,robotsRequired):
        self.id = id
        self.location = location
        self.time = time
        self.task = task
        self.robotsRequired = robotsRequired
        self.completed = False
        self.assigned = []
        self.ready = []
    def getLocation(self):
        return self.location  
    def getTime(self):
        return self.time
    def getTask(self):
        return self.task
    def getReady(self):
        return self.ready
    def getrobotsRequired(self): 
        return self.robotsRequired
    def deassignRobot(self,robot):
        if robot in self.assigned:
            self.assigned.remove(robot)
        if robot in self.ready:
            self.ready.remove(robot)
    def assignRobot(self,robot):
        if robot not in self.assigned:
            self.assigned.append(robot)
      
    def getAssigned(self):
        return self.assigned
    def readyRobot(self,robot):
        if robot not in self.ready:
            self.ready.append(robot)
    def completion(self):
        return self.completed
    def robotMessage(self):
        return {"Location":self.location,"Time":self.time,"Task":self.task}
    def severInfoMessage(self):
        return {"id":self.id,"location":self.location,"time":self.time,"task":self.task,"robots required":self.robotsRequired,"completed":self.completed,"assigned":self.assigned}