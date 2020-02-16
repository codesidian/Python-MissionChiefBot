class Despatch:
    #ID - Mission ID (String)
    #vehicles - List of vehicle ID's sent to mission
    #remSec - Remaining time in seconds
    def __init__(self, ID,vehicles, remSec):
        self.ID = ID
        self.vehicles = vehicles
        self.remSec = remSec

    def getID(self):
        return self.ID
    def getVehicles(self):
        return self.vehicles
    def __eq__(self, other):
        return self.ID == other.ID