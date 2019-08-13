from Objects import Coordinate, TimeNode, ODNode, PathNode, HashTable, ODRegion
from datetime import datetime, timedelta
import sys
import csv
import time
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt




def getODNodesFromFile(fileName: str, timeInterval: int):
    """

    :param fileName: the name of the file to get the info
    :return: a list of all the od nodes the file contained
    """

    '''list of od nodes'''
    ODNodes = []

    with open(fileName, 'r') as inputfile17:

        for line in inputfile17:
            line = line.strip()

            '''get the general attributes from the outputfile'''
            if line.__contains__("Total Trips"):
                totalTripCount = int(line[13:])
            if line.__contains__("Int Trips"):
                interestTripCount = int(line[13:])
            if line.__contains__("OD Maps"):
                odMapCount = int(line[13:])
            if line.__contains__("Time Maps"):
                timeMapCount = int(line[13:])
            if line.__contains__("Path Maps"):
                pathMapCount = int(line[13:])

            '''if we are looking at a new od node'''
            while line.__contains__("Index"):

                '''get the origin of the od node'''
                voriginLine = inputfile17.readline().strip()
                if voriginLine == '':
                    break

                vorigin = voriginLine[8:]
                vcommaIndex = vorigin.index(",")
                voriginLat = vorigin[:vcommaIndex]
                voriginLong = vorigin[vcommaIndex + 1:]
                voriginC = Coordinate.Coordinate(float(voriginLat), float(voriginLong))

                '''get the destination of the od node'''
                vdestLine = inputfile17.readline().strip()
                vdestination = vdestLine[13:]
                vcommaIndex = vdestination.index(",")
                vdestlat = vdestination[:vcommaIndex]
                vdestlong = vdestination[vcommaIndex + 1:]
                vdestC = Coordinate.Coordinate(float(vdestlat), float(vdestlong))

                '''readout the direction'''
                direction = inputfile17.readline()

                '''get the count of the od node'''
                vcountLine = inputfile17.readline().strip()
                vcount = vcountLine[7:]

                '''get the am count of the od node'''
                vamCountLine = inputfile17.readline().strip()
                vamCount = vamCountLine[9:]

                '''get the pm count of the od node'''
                vpmCountLine = inputfile17.readline().strip()
                vpmCount = vpmCountLine[9:]

                '''create the od node'''
                vodnode = ODNode.ODNode(voriginC, vdestC, int(vcount))

                '''update the period counts of the od node'''
                vodnode.setAmCount(int(vamCount))
                vodnode.setPmCount(int(vpmCount))

                '''set the direction of the node'''
                if direction.__contains__("In-"):
                    vodnode.setInbound(True)
                else:
                    vodnode.setInbound(False)

                '''readout the "Times: "'''
                readOut = inputfile17.readline().strip()

                '''update the times of the od node'''
                vt = inputfile17.readline().strip()

                '''for all the timenodes listed'''
                while vt.__contains__("WeekDay"):
                    '''get the weekday, time, and count'''
                    weekday = int(vt[9:11])
                    vtime = vt[19:24]
                    vcount = int(vt[32:])

                    '''create the TimeNode'''
                    vdt = datetime.strptime(vtime, "%H:%M")
                    vtimenode = TimeNode.TimeNode(vdt, weekday, timeInterval)
                    vtimenode.setCount(vcount)

                    '''the dict to be used as the dict of paths for timenode'''
                    paths = {}

                    '''read the next line in the file'''
                    nl = inputfile17.readline().strip()

                    # changed the output of the hashtable to be correct
                    if nl.__contains__("Paths"):

                        nl = inputfile17.readline().strip()

                        while nl.__contains__("PathID"):
                            '''get the PathNode attributes'''
                            countIndex = nl.index("Count:")
                            path = nl[8:countIndex - 1]
                            count = nl[countIndex + 7:]

                            '''create the pathNode'''
                            pathNode = PathNode.PathNode(path)
                            pathNode.setCount(int(count))

                            '''add the PathNode to the dict of PathNodes'''
                            paths[path] = pathNode

                            nl = inputfile17.readline().strip()

                        vt = nl

                    '''set the paths of the time node'''
                    vtimenode.setPaths(paths)

                    vt = nl
                    '''add the time node to the list of times in od node'''
                    vodnode.addTimeNode(vtimenode)

                if vt.__contains__("Index"):
                    line = vt

                '''add the od node to the list of od nodes'''
                '''only if it is not an empty node'''
                e = Coordinate.Coordinate(0, 0)
                empty = ODNode.ODNode(e, e, 0)
                if vodnode.__eq__(empty) is False:
                    ODNodes.append(vodnode)

    inputfile17.close()

    return ODNodes


def matchCoordinates(fileName: str):

    matchedCoordinates = []

    try:
        with open(fileName, 'r', newline='') as file:
            reader = csv.reader(file)

            for l in reader:
                c = Coordinate.Coordinate(l[0], l[1])
                c.setDistrict(l[2])
                matchedCoordinates.append(c)

        file.close()

    except:
        print("Error opening file in matchCoordinates()")

    return matchedCoordinates


def createRegions(fileName: str):
    """

    :param fileName: name of the file that contains coordinates mapped to regions
    :return: a list of all possible regions
    """

    regions = []

    nova = {}
    dc = {}

    with open(fileName, 'r', newline='') as f:
        reader = csv.reader(f)

        for line in reader:

            district = str(line[2])

            if district.__contains__("NOVA"):
                nova[district] = 0
            if district.__contains__("DC"):
                dc[district] = 0
    f.close()

    for n in nova:
        for d in dc:
            inbound = ODRegion.ODRegion(n, d, True)
            regions.append(inbound)
    for d in dc:
        for n in nova:
            outbound = ODRegion.ODRegion(d, n, False)
            regions.append(outbound)

    for r in regions:
        r.createTimeIntervals("00:00", "23:59", 30)

    return regions


def attachRegions(nodes: list, coords: list):
    """

    :param nodes: a list of all the od nodes with all the data
    :param coords: a list of all the coordinates matched to a region
    :return:
    """

    '''loop through all passed nodes'''
    for node in nodes:
        '''loop though all coordinates that are matched to regions'''
        for coor in coords:
            '''snap the region to the coordinates of the od node'''
            d = coor.getDistrict()
            if node.origin.equals(coor):
                node.origin.setDistrict(d)
            if node.destination.equals(coor):
                node.destination.setDistrict(d)


    nodesWithRegions = []

    for node in nodes:
        if node.origin.getDistrict() != "blank" and node.destination.getDistrict() != "blank":
            nodesWithRegions.append(node)

    return nodesWithRegions


def updateRegions(regions: list, nodes: list):
    """

    :param regions: the regions to be updated
    :param nodes: the od nodes used to update the regions
    :return: a list of updated regions
    """

    for node in nodes:
        for r in regions:

            regionTimes = r.getTimes()

            if node.origin.getDistrict() == r.getOrigin():
                if node.destination.getDistrict() == r.getDestination():
                    '''update region'''
                    '''update the counts'''
                    r.setCount(r.getCount() + node.getCount())
                    r.setAMCount(r.getAmCount() + node.getAmCount())
                    r.setPMCount(r.getPmCount() + node.getPmCount())

                    '''update the time counts'''
                    nodeTimes = node.getTimes()
                    for t in nodeTimes:
                        nodeTimeNode = nodeTimes[t]
                        if regionTimes.__contains__(t):
                            regionTimeNode = regionTimes[t]

                            '''update the time count'''
                            regionTimeNode.setCount(regionTimeNode.getCount() + nodeTimeNode.getCount())

                            '''update the paths'''
                            nodeTimeNodePaths = nodeTimeNode.getPaths()
                            regionTimeNodePaths = regionTimeNode.getPaths()
                            for p in nodeTimeNodePaths:

                                # the actual path node from the time node
                                nodeTimeNodePath = nodeTimeNodePaths[p]

                                # if the region time already has seen this path, update it
                                if regionTimeNodePaths.__contains__(p):

                                    regionTimeNodePath = regionTimeNodePaths[p]

                                    regionTimeNodePath.setCount(regionTimeNodePath.getCount() + nodeTimeNodePath.getCount())

                                    regionTimeNodePaths[p] = regionTimeNodePath

                                # if the region time node has not already seen this path, add it
                                else:
                                    regionTimeNodePaths[p] = nodeTimeNodePath

                            regionTimes[t] = regionTimeNode

    return regions


def setUpRegions(nodes: list):
    """

    :param nodes: list of od nodes that contain all the data
    :return: the counts for each region
    """

    matchedCoordinates = matchCoordinates("ActualGridToRegion.csv")

    # what regions are we working with
    regions = createRegions("ActualGridToRegion.csv")

    # attach regions to the coordinates of the od nodes
    nodesWithRegions = attachRegions(nodes, matchedCoordinates)

    # go through all the od nodes, and add its counts to the correct regions counts
    updatedRegions = updateRegions(regions, nodesWithRegions)

    return updatedRegions


def two_proprotions_test(success_a, size_a, success_b, size_b):
    """
    A/B test for two proportions;
    given a success a trial size of group A and B compute
    its zscore and pvalue

    Parameters
    ----------
    success_a, success_b : int
        Number of successes in each group

    size_a, size_b : int
        Size, or number of observations in each group

    Returns
    -------
    zscore : float
        test statistic for the two proportion z-test

    pvalue : float
        p-value for the two proportion z-test
    """
    prop_a = success_a / size_a
    prop_b = success_b / size_b
    prop_pooled = (success_a + success_b) / (size_a + size_b)
    var = prop_pooled * (1 - prop_pooled) * (1 / size_a + 1 / size_b)
    zscore = np.abs(prop_b - prop_a) / np.sqrt(var)
    one_side = 1 - stats.norm(loc=0, scale=1).cdf(zscore)
    pvalue = one_side * 2
    return zscore, pvalue


def regionCountAnalysis(regions17: list, regions18: list):
    """

    :param regions17: the 2017 regions
    :param regions18: the 2018 regions
    :return: a list of lists containing the origin, destination, z score, and p value
    """

    # this is the list of lists to be returned
    masterList = []

    size17 = 0
    for i in regions17:
        size17 += i.getCount()

    size18 = 0
    for i in regions18:
        size18 += i.getCount()

    for a in regions17:
        for b in regions18:
            if a.origin == b.origin and a.destination == b.destination:

                zscore, pvalue = two_proprotions_test(a.getCount(), size17, b.getCount(), size18)
                subList = [a.origin, a.destination, zscore, round(pvalue, 5)]

                masterList.append(subList)

    return masterList


def completePathCountAnalysis(regions17: list, regions18: list):
    """

    :param regions17: the 2017 regions
    :param regions18: the 2018 regions
    :return: a list of lists containing the origin, destination, z score, and p value
    """

    # this is the list of lists to be returned
    masterList = []

    size17 = 0
    for i in regions17:
        size17 += i.getCount()

    size18 = 0
    for i in regions18:
        size18 += i.getCount()

    for a in regions17:
        for b in regions18:

            # if we are looking at the same region
            if a.origin == b.origin and a.destination == b.destination:

                times17 = a.getTimes()
                times18 = b.getTimes()

                for c in times17.values():
                    for d in times18.values():

                        # if we are looking at the same time node
                        if c.getWeekDay() == d.getWeekDay():
                            if c.getTimeID() == d.getTimeID():

                                paths17 = c.getPaths()
                                paths18 = d.getPaths()

                                for e in paths17.values():
                                    for f in paths18.values():

                                        # if they both have the path
                                        if e.getPathID() == f.getPathID():
                                            zscore, pvalue = two_proprotions_test(e.getCount(), size17,
                                                                                  f.getCount(), size18)
                                            smallList = [a.origin, a.destination, c.getWeekDay(), c.getTimeID(),
                                                         e.getPathID(), zscore, pvalue]

                                            masterList.append(smallList)

                                            break

                                        # if only 17 has the path



    return masterList

def filterPaths(regions: list):

    newRegions = []
    for r in regions:
        for t in r.getTimes().values():
            paths = t.getPaths()
            for p in paths:
                pathNode = paths
                if pathNode.getPathID().__contains__("---"):
                    del paths[p]
        newRegions.append(r)

    return newRegions

def main():

    sys.argv.pop(0)
    inputFile17 = sys.argv.pop(0)
    inputFile18 = sys.argv.pop(0)
    outputFile = sys.argv.pop(0)


    print("Creating Nodes...")
    # create the 2017 od nodes
    ODNodes17 = getODNodesFromFile(inputFile17, 30)
    # create the 2018 od nodes
    ODNodes18 = getODNodesFromFile(inputFile18, 30)
    print("Nodes Created")

    print("Creating Regions...")
    # create the 2017 regions
    regions17 = setUpRegions(ODNodes17)
    regions17 = filterPaths(regions17)
    # create the 2018 regions
    regions18 = setUpRegions(ODNodes18)
    regions18 = filterPaths(regions18)
    print("Regions Created")


    # analyze the region count
    print("count analysis")
    regionalCountAnalysis = regionCountAnalysis(regions17, regions18)
    with open("STATregionalCountAnalysis.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(regionalCountAnalysis)
    file.close()

    # analyze the path counts
    # year to year

    # relative to od region
    # relative to od region and morning and afternoon
    # relative to od region and thirty min time interval
    print("complete path count analysis")
    completePathAnalysis = completePathCountAnalysis(regions17, regions18)
    with open("STATCompletePathAnalysis.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(completePathAnalysis)
    file.close()



    print("Done.")


main()

# end of file
