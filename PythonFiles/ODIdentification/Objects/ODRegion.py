from Objects import ODNode, Coordinate

class ODRegion:

    def __init__(self, origin: str, dest: str, inbound: bool):
        self.origin = origin
        self.destination = dest
        self.inbound = inbound
        self.ODNodes = []
        self.count = 0
        self.amCount = 0
        self.pmCount = 0
        self.location = Coordinate.Coordinate(0, 0)

    def toString(self):
        return "From: " + str(self.origin) + "\tTo : " + str(self.destination)

    def getLocation(self):
        return self.location
    def setLocation(self, c: Coordinate):
        self.location = c

    def getOrigin(self):
        return self.origin

    def getDestination(self):
        return self.destination

    def getInbound(self):
        return self.inbound

    def addODNode(self, n: ODNode):
        self.ODNodes.append(n)

    def getODNode(self):
        return self.ODNodes
    def getCount(self):
        return self.count
    def getAMCount(self):
        return self.amCount
    def getPMCount(self):
        return self.pmCount
    def setCount(self, i):
        self.count = i
    def setAMCount(self, i):
        self.amCount = i
    def setPMCount(self, i):
        self.pmCount = i



# end of file
