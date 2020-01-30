class Vehicle:
    def __init__(self, ID,name,vType,status):
        self.name = name
        self.ID = ID
        self.status = status
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
        self.status = status
    def __eq__(self, other):
        return self.ID == other.ID
