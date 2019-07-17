from Objects import Coordinate, ODNode
import hashlib

PYTHONHASHSEED = 0


def find_next_prime(na):
    return find_prime_in_range(na, 2*na)


def find_prime_in_range(a, b):
    for p in range(a, b):
        for i in range(2, p):
            if p % i == 0:
                break
        else:
            return p
    return None


class HashTable:
    """The main problem with this hashtable is that when using the contains or find method, the object
    you are looking for do not have the same hashFunction exactly.  This is because we are looking at if the
    passed node is close to any of the nodes in the grid.  This means that the contains method cannot stop if it finds
    an empty spot.  The hash table would be much more efficient if close nodes had the same hashcode"""

    def __init__(self, num: int, factor: int = 2):
        """num is the number of elements the table needs to hold, not the size of the table
        factor is the loading factor for the hashtable, the size and speed of the table increase as this increases
        a factor of 2 is normal, 3 is faster and requires more space"""

        # the size of the hashTable, must be prime
        size = find_next_prime(num*factor)

        dummyCoordinate = Coordinate.Coordinate(0, 0)
        dummyNode = ODNode.ODNode(dummyCoordinate, dummyCoordinate, 0)

        '''create the array'''
        table = []
        self.table = table
        for dumbNode in range(0, size):
            table.append(dummyNode)

    def insert(self, noder: ODNode):

        # get the hash code for the passed object
        hashCode = self.getHash(noder)

        # how many collisions there have been trying to insert this node
        collisionCounter = 0

        # the index to search at
        search = (hashCode + collisionCounter**2) % self.table.__len__()

        # add the passed object to the table (array)
        # the node that shows that the index is open
        empty = Coordinate.Coordinate(0, 0)

        added = False

        # while the spot is not empty
        for itera in range(0, self.table.__len__()):

            '''if the spot is not empty, go to the next spot'''
            if self.table[search].origin.__eq__(empty) is False and \
                    self.table[search].destination.__eq__(empty) is False:

                # incemenet the number of collisions
                collisionCounter += 1

                # update the search index
                search = (hashCode + collisionCounter**2) % self.table.__len__()

        # add the node to the correct index
        self.table[search] = noder

    # will return true if there is a node that is close to the given node
    # dist is the tolerance to the node
    def __contains__(self, noder: ODNode, odist, ddist):

        # get the hash code for the passed object
        hashCode = self.getHash(noder)

        # how many collisions there have been trying to insert this node
        collisionCounter = 0

        # the index to search at
        search = (hashCode + collisionCounter**2) % self.table.__len__()

        checked = []

        # while the spot is not close to the node
        while self.table[search].origin.close(noder.origin, odist) is False & \
                self.table[search].destination.close(noder.destination, ddist) is False:

            checked.append(search)

            # if every spot has been searched
            if collisionCounter == self.table.__len__():
                return False

            # incemenet the number of collisions
            collisionCounter += 1

            # update the search index
            search = (hashCode + collisionCounter**2) % self.table.__len__()

        return True

    def getIndex(self, node: ODNode, odist, ddist):
        """

        :param node: the OD node we are looking for
        :param odist: the distance tolerance for origin nodes
        :param ddist: the distance tolerance for dest nodes
        :return: the index of the ODNode in the hashtable the passed node is close to
        """

        # get the hash code for the passed object
        hashCode = self.getHash(node)

        # how many collisions there have been trying to insert this node
        collisionCounter = 0

        # the index to search at
        search = (hashCode + collisionCounter ** 2) % self.table.__len__()

        # while the spot is not close to the node
        while self.table[search].origin.close(node.origin, odist) is False & \
                self.table[search].destination.close(node.destination, ddist) is False:
            # incemenet the number of collisions
            collisionCounter += 1

            # update the search index
            nxt = collisionCounter
            search = (hashCode + nxt) % self.table.__len__()

        # add the node to the correct index
        return search



    # it is the programmers responsibility to run the contains method before running this
    # will return the first node it finds that is close to the passed node
    def find(self, nodea: ODNode, odist, ddist):

        # get the hash code for the passed object
        hashCode = self.getHash(nodea)

        # how many collisions there have been trying to insert this node
        collisionCounter = 0

        # the index to search at
        search = (hashCode + collisionCounter**2) % self.table.__len__()

        # while the spot is not close to the node
        while self.table[search].origin.close(nodea.origin, odist) is False & \
                self.table[search].destination.close(nodea.destination, ddist) is False:

            # incemenet the number of collisions
            collisionCounter += 1

            # update the search index
            nxt = collisionCounter
            search = (hashCode + nxt) % self.table.__len__()

        # add the node to the correct index
        return self.table[search]

    # a second hash function
    def getHashTwo(self, noda: ODNode):
        return hash(noda.toString())

    # the hash function
    def getHash(self, node: ODNode):

        # hashCode = hash(nodee.origin.toString()) + hash(nodee.destination.toString())
        # hashCode = hash(hashCode)
        # hashCode = hash(node.toString())

        coder = hashlib.sha1()
        encodedString = node.toString().encode()
        coder.update(encodedString)
        hashCode = coder.hexdigest()
        hashCode = int(hashCode, 16)


        return hashCode

    def toString(self):
        string = "HashTable: "

        # the empty node, sigals no element at this index
        empty = ODNode.ODNode(Coordinate.Coordinate(0, 0), Coordinate.Coordinate(0, 0), 0)

        index = 0

        '''iterate through the odnodes'''
        for odnode in self.table:
            if odnode.__eq__(empty) is False:
            # if True:
                if odnode.getCount() >= 0:
                    string = string + ("\nIndex[" + str(index) + "]")

                    '''the to string method of the odnode'''
                    string = string + \
                             "\n\tOrigin: " + odnode.origin.toString() + \
                             "\n\tDestination: " + odnode.destination.toString() + \
                             "\n\tCount: " + str(odnode.count) + \
                             "\n\tAMCount: " + str(odnode.getAmCount()) + \
                             "\n\tPMCount: " + str(odnode.getPmCount()) + \
                             "\n\tTimes:"

                    '''iterate through timenodes'''
                    for time in odnode.times:
                        timeNode = odnode.times[time]
                        timeNodePaths = timeNode.getPaths()

                        '''only print if the count is not 0'''
                        if timeNode.getCount() > 0:
                            add = "\n\t\tWeekDay: " + str(timeNode.getWeekDay()) + " TimeID: " + \
                                    str(timeNode.getTimeID()) + " Count: " + str(timeNode.getCount())
                            string = string + add

                            if len(timeNodePaths) > 0:

                                string = string + "\n\t\tPaths:"
                                # for each time iterate through all of the trips
                                for path in timeNodePaths:
                                    pathNode = timeNodePaths[path]
                                    more = "\n\t\t\tPathID: " + str(pathNode.getPathID()) + " Count: " + str(
                                        pathNode.getCount())
                                    string = string + more
            index += 1

        return string

    def print(self):

        # the empty node, sigals no element at this index
        empty = ODNode.ODNode(Coordinate.Coordinate(0, 0), Coordinate.Coordinate(0, 0), 0)

        index = 0

        print("HashTable: ")
        for this in self.table:
            if this.__eq__(empty) is False:
                if this.getCount() > 0:
                    print("Index[" + str(index) + "] " + this.toString())
            index += 1


# end of file
