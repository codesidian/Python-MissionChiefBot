class Mission:
    #ID - Mission ID (String)
    #name - Mission Name (String)
    #requirements - Mission Requirements (list)
    #status - Mission Status (int)
    def __init__(self, ID,name,requirements,status=0):
        self.name = name
        self.ID = ID
        self.requirements = requirements
        self.status=status

        
    def getName(self):
        return self.name
    def getID(self):
        return self.ID
    def getStatus(self):
        return self.status
    def setStatus(self, status):
        self.status = status
    def getRequirements(self):
        return self.requirements
    def __eq__(self, other):
        return self.ID == other.ID
