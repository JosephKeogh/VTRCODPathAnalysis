from Objects import Coordinate, TimeNode
from datetime import datetime, timedelta


class ODNode:

    # methods
    # the constructor takes two coordinates as inputs
    def __init__(self, origin1: Coordinate, destination1: Coordinate, count1):

        # the coordinates of the unique origin and destination combination for this node
        self.origin = origin1
        self.destination = destination1

        # how many times this OD node has been used
        self.count = int(count1)

        # a list of the times this node will cover
        # using a dict because each time will be unique
        # this is list of time nodes
        times = {}
        self.times = times

        # the count of how many times this node was seen during peak periods
        self.amCount = 0
        self.pmCount = 0

        # the direction of the node
        self.inbound = True


    """getters and setters"""

    def setInbound(self, d: bool):
        self.inbound = d

    def getInbound(self):
        return self.inbound

    def setCount(self, num):
        self.count = num

    def getCount(self):
        return self.count

    def setTimes(self, l):
        self.times = l

    def getTimes(self):
        return self.times

    def getAmCount(self):
        return self.amCount

    def getPmCount(self):
        return self.pmCount

    def setAmCount(self, num: int):
        self.amCount = num

    def setPmCount(self, num: int):
        self.pmCount = num

    """typicals"""

    def incAmCount(self):
        self.amCount += 1

    def incPmCount(self):
        self.pmCount += 1

    def toString(self):
        string = ""
        string = string + \
                 "Origin: " + self.origin.toString() + \
                 "\nDestination: " + self.destination.toString() + \
                 "\nCount: " + str(self.count) + \
                 "\nAMCount: " + str(self.getAmCount()) + \
                 "\nPMCount: " + str(self.getPmCount()) + \
                 "\nTimes:"

        # iterate through all of the times
        for time in self.times:
            timeNode = self.times[time]
            timeNodePaths = timeNode.getPaths()

            '''only print if the count is not 0'''
            if timeNode.getCount() > 0:
                add = "\n\tTimeID: " + str(timeNode.getTimeID()) + " Count: " + str(timeNode.getCount())
                string = string + add

                if len(timeNodePaths) > 0:

                    string = string + "\n\tPaths:"
                    # for each time iterate through all of the trips
                    for trip in timeNodePaths:
                        tripNode = timeNodePaths[trip]
                        more = "\n\t\tPathID: " + str(tripNode.getPathID()) + " Count: " + str(
                            tripNode.getCount())
                        string = string + more
        return string

    def toStringShort(self):
        """returns a more compact version of the toString method"""
        return "O: " + self.origin.toStringShort() + " D: " + self.destination.toStringShort() + \
               "Count: " + str(self.count)

    def print(self):
        """prints the attributes of the ODNode"""
        print(self.toString())

    def __eq__(self, other):
        if self.origin.__eq__(other.origin):
            if self.destination.__eq__(other.destination):
                return True
            else:
                return False
        else:
            return False


    """methods"""

    """all the time intervals to be looked at"""
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

    def addTimeNode(self, timeNode: TimeNode):
        """add a TimeNode to the list of TimeNodes for this ODNode"""
        self.times[timeNode.getTimeID() + str(timeNode.getWeekDay())] = timeNode

    def inc(self):
        self.count += 1

    def __contains__(self, node: TimeNode) -> bool:
        if node in self.times.values():
            return True
        else:
            return False

    def findTime(self, item: TimeNode) -> TimeNode:
        # todo this probably takes up a lot of time

        for node in self.times.values():
            if node.__eq__(item):
                return node


        n = self.times[item.getTimeID() + str(item.getWeekDay())]

        return n


def timeToInt(time: str):
    """returns the time passed to the integer of how many minutes have passed that day"""

    """the current hour and min"""
    hour = time[0:2]
    min = time[3:]

    hourInt = int(hour) * 60
    minInt = int(min)

    return hourInt + minInt
# main
# end of file
