from Objects import PathNode
from datetime import datetime, timedelta


class TimeNode:

    def __init__(self, dateTime: datetime, dayOfWeek: int,  timeTolerance: int):
        """
            time is the time of day this node will represent
            should this be only in time (ex: 0900) or should it be a date
            will probably do analysis based on weeks - proportion of people traveling on given path per week
            so will want data, not just time
        """
        # the time identifier
        time = datetime.strftime(dateTime, "%H:%M")
        self.timeID = time

        # the day of the week
        self.weekday = dayOfWeek

        # a list of paths, using dict becuase the pathIDs will be unique
        # a list of path nodes
        # key is the path ID, value is the path node
        a = {}
        self.paths = a

        # a list of trip ids
        b = {}
        self.tripIDs = b

        self.count = 0

        self.timeTolerance = timeTolerance

    """getters and setters"""
    def getTimeID(self):
        return self.timeID

    def getPaths(self):
        return self.paths

    def getCount(self):
        return self.count

    def getTripIDs(self):
        return self.tripIDs

    def getWeekDay(self):
        return self.weekday

    def setCount(self, c: int):
        self.count = c

    def getTolerance(self):
        return self.timeTolerance

    def setPaths(self, d: dict):
        self.paths = d

    """typicals"""
    def toString(self):
        string = "WeekDay: " + str(self.getWeekDay()) + " TimeID: " + str(self.timeID) + \
                 " Count: " + str(self.count) + "\n" + "Trips: "
        for item in self.paths:
            string = string + "\n\t" + self.paths[item].toString()
        return string

    def __eq__(self, other):
        """
        if same day of week, and same time, then true
        :param other: the other node to compare
        :return:
        """

        node1 = timeToInt(self.getTimeID())
        node2 = timeToInt(other.getTimeID())

        diff = abs(node1 - node2)

        if diff < self.timeTolerance:
            if self.getWeekDay() == other.getWeekDay():
                return True
            else:
                return False
        else:
            return False



    """methods"""
    def inc(self):
        self.count += 1

    def addTripID(self, tripID):
        self.tripIDs[tripID] = 0

    def addPath(self, node: PathNode):
        """takes the passed trip node and adds it to the list of trips"""
        self.paths[node.getPathID()] = node

    def contains(self, pathNode: PathNode):
        """returns true if the time node already contains the trip node passed"""
        # todo
        if pathNode.getPathID() in self.paths:
            return True
        else:
            return False

    def findPath(self, pathNode: PathNode):
        """this method will return the node passed that is in the list of trips"""
        # todo
        return self.paths[pathNode.getPathID()]


def timeToInt(time: str):
    """returns the time passed to the integer of how many minutes have passed that day"""

    """the current hour and min"""
    hour = time[0:2]
    min = time[3:]

    hourInt = int(hour) * 60
    minInt = int(min)

    return hourInt + minInt

# main--------------------------------------------------------------------

# end of file
