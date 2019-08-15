class PathNode:

    def __init__(self, pathID: str):
        """
            the tripID is not for individual trips, but rather the path
        :param tripID: str - name of the path that is take
        :return TripNode
        """
        self.pathID = pathID
        self.count = 0

    """getters and setters"""
    def getPathID(self):
        """

        :return: the PathID
        """
        return self.pathID

    def getCount(self):
        """

        :return: the count of how many times we have seen this tripNode
        """
        return self.count

    def setCount(self, num: int):
        """
        set a new count for the TripNode
        :param num: the new count
        """
        self.count = num

    """typicals"""
    def __eq__(self, other):
        if self.pathID == other.getPathID():
            return True
        else:
            return False

    def toString(self):
        """returns the info about the node"""
        return "PathID: " + str(self.pathID) +\
            " Count: " + str(self.count)


    """methods"""
    def inc(self):
        self.count += 1


# main --------------


# end of file
