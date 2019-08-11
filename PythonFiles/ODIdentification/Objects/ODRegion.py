from Objects import ODNode, Coordinate, PathNode, TimeNode
from datetime import datetime, timedelta

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
        self.paths = {}
        self.times = {}

    '''getters and setters'''
    def getTimes(self):
        return self.times

    def getLocation(self):
        return self.location

    def getOrigin(self):
        return self.origin

    def getDestination(self):
        return self.destination

    def getInbound(self):
        return self.inbound

    def getODNode(self):
        return self.ODNodes

    def getCount(self):
        return self.count

    def getAmCount(self):
        return self.amCount

    def getPmCount(self):
        return self.pmCount

    def setTimes(self, t: dict):
        self.times = t

    def setLocation(self, c: Coordinate):
        self.location = c

    def setCount(self, i):
        self.count = i

    def setAMCount(self, i):
        self.amCount = i

    def setPMCount(self, i):
        self.pmCount = i

    '''typicals'''

    def toString(self):
        string = ""

        direction = "Out-Bound"

        if self.getInbound() is True:
            direction = "In-Bound"

        '''the to string method of the odnode'''
        string = string + \
                 "\nOrigin: " + self.origin + \
                 "\nDestination: " + self.destination + \
                 "\nDirection: " + direction + \
                 "\nCount: " + str(self.count) + \
                 "\nAMCount: " + str(self.getAmCount()) + \
                 "\nPMCount: " + str(self.getPmCount()) + \
                 "\nTimes:"

        '''iterate through timenodes'''
        for time in self.times:
            timeNode = self.times[time]
            timeNodePaths = timeNode.getPaths()

            '''only print if the count is not 0'''
            if timeNode.getCount() > 0:
                add = "\n\tWeekDay: " + str(timeNode.getWeekDay()) + " TimeID: " + \
                      str(timeNode.getTimeID()) + " Count: " + str(timeNode.getCount())
                string = string + add

                if len(timeNodePaths) > 0:

                    string = string + "\n\tPaths:"
                    # for each time iterate through all of the trips
                    for path in timeNodePaths:
                        pathNode = timeNodePaths[path]
                        more = "\n\t\tPathID: " + str(pathNode.getPathID()) + " Count: " + str(
                            pathNode.getCount())
                        string = string + more

        return string

    def toStringShort(self):
        return "From: " + self.getOrigin() + " To: " + self.getDestination()


    '''methods'''

    def updatePath(self, node: PathNode):

        id = node.getPathID()

        if self.paths.__contains__(id):

            old = self.paths[id]
            old.setCount(node.getCount() + old.getCount())

            self.paths[id] = old

        else:

            self.paths[id] = node

    def addODNode(self, n: ODNode):
        self.ODNodes.append(n)

    def addTimeNode(self, timeNode: TimeNode):
        """add a TimeNode to the list of TimeNodes for this ODNode"""
        self.times[timeNode.getTimeID() + str(timeNode.getWeekDay())] = timeNode

    def createTimeIntervals(self, startTime: str, endTime: str, interval: int):

        currTime = startTime

        '''create the time intervals'''
        while timeToInt(currTime) < timeToInt(endTime):
            """is < and not <- becuase this way we will not map anything past the endTime"""
            '''for every day of the week'''
            for i in range(0, 7):
                """create a timenode and add it to the list of timenodes"""
                currDateTime = datetime.strptime(currTime, "%H:%M")
                timeNode = TimeNode.TimeNode(currDateTime, i, interval)
                self.addTimeNode(timeNode)

            """the current hour and min"""
            hour = currTime[0:2]
            min = currTime[3:]

            """update the current time"""
            minInt = int(min)
            newMinInt = minInt + interval

            """if the minutes go over 60 go to the next hour"""
            if newMinInt >= 60:
                hourInt = int(hour)
                newHourInt = hourInt + 1
                newHour = str(newHourInt)

                newMinInt = newMinInt % 60
                newMin = str(newMinInt)

            else:
                newHour = hour
                newMin = str(newMinInt)

            """times need to be the proper length"""
            if newHour.__len__() < 2:
                newHour = "0" + newHour
            if newMin.__len__() < 2:
                newMin = "0" + newMin

            currTime = newHour + ":" + newMin



def timeToInt(time: str):
    """returns the time passed to the integer of how many minutes have passed that day"""

    """the current hour and min"""
    hour = time[0:2]
    min = time[3:]

    hourInt = int(hour) * 60
    minInt = int(min)

    return hourInt + minInt

# end of file
