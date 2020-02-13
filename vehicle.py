class Vehicle:
    #name - Vehicle Name (String)
    #id - Vehicle ID (String)
    #status - Vehicles Status (String)
    #vType - Type of Vehicle (String)
    
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
    # 1 = FREE 2 = FREE 3 = DESPATCHED
    def setStatus(self, status):
        self.status = status
    def despatchable(self):
        if self.getStatus() == '1' or self.getStatus() == '2':
            return True
        else:
            return False
    def setDespatched(self): 
        self.setStatus('3')
        return True

    def __eq__(self, other):
        return self.ID == other.ID
