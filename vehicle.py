class Vehicle:
    def __init__(self, ID,name,vType,status):
        self.name = name
        self.ID = ID
        self.status= status
        self.vType = vType
        
    def getName(self):
        return self.name
    def getID(self):
        return self.ID
    def getStatus(self):
        return self.status
    def getType(self):
        return self.vType
    def setStatus(self, status):
        # 0 = Not attempted, 1 = Partly despatched, 2 = Fully completed.
        self.status = status

    def availableDespatch(self):
        if(self.getStatus()=="1" or self.getStatus()=="2"):
            return True
        else:
            return False