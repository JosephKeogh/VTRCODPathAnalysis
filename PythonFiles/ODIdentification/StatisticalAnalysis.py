from Objects import Coordinate, TimeNode, ODNode, PathNode, HashTable, ODRegion
from datetime import datetime, timedelta
import sys
import csv
import time
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt



def timeToInt(now):
    """

    :param time: the time in "00:00"
    :return: an int of how many minutes have passed that day
    """

    """the current hour and min"""
    hour = now[0:2]
    min = now[3:]

    hourInt = int(hour) * 60
    minInt = int(min)

    return hourInt + minInt


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


def filterPaths(regions: list):
    """

    :param regions: the regions to have their paths filterd
    :return: a list of regions will all the paths mapped to multiple paths
    taken out
    """
    newRegions = []
    for r in regions:
        for t in r.getTimes().values():
            paths = t.getPaths()
            newPaths = {}
            for p in paths:
                pathNode = paths[p]
                if pathNode.getPathID().__contains__("---") is False:
                    newPaths[p] = paths[p]
            t.setPaths(newPaths)
        newRegions.append(r)

    return newRegions


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


def pathCountAnalysis(regions17: list, regions18: list):
    """

    :param regions17:
    :param regions18:
    :return:
    """

    masterList = []

    masterList.append(["Path", "zscore", "pvalue"])

    paths17 = {}
    pathCount17 = 0
    paths18 = {}
    pathCount18 = 0

    for r in regions17:

        times = r.getTimes()

        for t in times:

            paths = times[t].getPaths()

            for p in paths:

                pathCount17 += paths[p].getCount()

                if paths17.__contains__(p):
                    master = paths17[p]
                    other = paths[p]
                    master.setCount(master.getCount() + other.getCount())

                else:
                    paths17[p] = paths[p]

    for r in regions18:

        times = r.getTimes()

        for t in times:

            paths = times[t].getPaths()

            for p in paths:

                pathCount18 += paths[p].getCount()

                if paths18.__contains__(p):
                    master = paths18[p]
                    other = paths[p]
                    master.setCount(master.getCount() + other.getCount())
                else:
                    paths18[p] = paths[p]

    # make it so each list of paths contains the same paths
    for e in paths17:
        if paths18.__contains__(e) is False:
            paths18[e] = PathNode.PathNode(e)
    for f in paths18:
        if paths17.__contains__(f) is False:
            paths17[f] = PathNode.PathNode(f)

    for p in paths17:
        pathNode17 = paths17[p]
        pathNode18 = paths18[p]
        zscore, pvalue = two_proprotions_test(pathNode17.getCount(), pathCount17,
                                              pathNode18.getCount(), pathCount18)
        smallList = [p, zscore, pvalue]
        masterList.append(smallList)

    return masterList


def regionCountAnalysis(regions17: list, regions18: list):
    """

    :param regions17: the 2017 regions
    :param regions18: the 2018 regions
    :return: a list of lists containing the origin, destination, z score, and p value
    """

    # this is the list of lists to be returned
    masterList = []

    masterList.append(["origin", 'destination', 'zscore', 'pvalue'])


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
    :return: a list of lists containing the origin, destination,
    day of week, time of day, path id,  z score, and p value
    """

    # this is the list of lists to be returned
    masterList = []

    masterList.append(["origin", 'destination', 'weekday', 'time', 'path', 'zscore', 'pvalue'])


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

                                # make it so each list of paths contains the same paths
                                for e in paths17:
                                    if paths18.__contains__(e) is False:
                                        paths18[e] = PathNode.PathNode(e)
                                for f in paths18:
                                    if paths17.__contains__(f) is False:
                                        paths17[f] = PathNode.PathNode(f)

                                for e in paths17:
                                    pathNode17 = paths17[e]
                                    pathNode18 = paths18[e]
                                    zscore, pvalue = two_proprotions_test(pathNode17.getCount(), a.getCount(),
                                                                          pathNode18.getCount(), b.getCount())
                                    smallList = [a.origin, a.destination, c.getWeekDay(), c.getTimeID(),
                                                 pathNode17.getPathID(), zscore, pvalue]

                                    masterList.append(smallList)

    return masterList


def regionPathCountAnalysis(regions17: list, regions18: list):
    """

    :param regions17: the 2017 regions
    :param regions18: the 2018 regions
    :return: a list of lists containing the origin, destination, path id,
     z score, and p value
    """

    # this is the list of lists to be returned
    masterList = []

    masterList.append(["origin", 'destination', 'path', 'zscore', 'pvalue'])


    size17 = 0
    for i in regions17:
        size17 += i.getCount()

    size18 = 0
    for i in regions18:
        size18 += i.getCount()

    for a in regions17:
        for b in regions18:

            rejectCount = 0

            masterpaths17 = {}
            masterpaths18 = {}

            # if we are looking at the same region
            if a.origin == b.origin and a.destination == b.destination:

                times17 = a.getTimes()
                times18 = b.getTimes()

                for t in times17.values():
                    paths = t.getPaths()
                    for p in paths:

                        # if we have already seen this path
                        if masterpaths17.__contains__(p):

                            # update the path
                            masterPathNode = masterpaths17[p]
                            pathNode = paths[p]
                            masterPathNode.setCount(masterPathNode.getCount() + pathNode.getCount())

                        # if we have not already seen this path
                        else:
                            masterpaths17[p] = paths[p]

                for t in times18.values():
                    paths = t.getPaths()
                    for p in paths:

                        # if we have already seen this path
                        if masterpaths18.__contains__(p):

                            # update the path
                            masterPathNode = masterpaths18[p]
                            pathNode = paths[p]
                            masterPathNode.setCount(masterPathNode.getCount() + pathNode.getCount())

                        # if we have not seen the path
                        else:
                            masterpaths18[p] = paths[p]

                # make it so each list of paths contains the same paths
                for e in masterpaths17:
                    if masterpaths18.__contains__(e) is False:
                        masterpaths18[e] = PathNode.PathNode(e)
                for f in masterpaths18:
                    if masterpaths17.__contains__(f) is False:
                        masterpaths17[f] = PathNode.PathNode(f)

                for e in masterpaths17:
                    pathNode17 = masterpaths17[e]
                    pathNode18 = masterpaths18[e]
                    zscore, pvalue = two_proprotions_test(pathNode17.getCount(), a.getCount(),
                                                          pathNode18.getCount(), b.getCount())
                    smallList = [a.origin, a.destination, pathNode17.getPathID(), zscore, pvalue]

                    if pvalue <= 0.05:
                        rejectCount += 1

                    masterList.append(smallList)

                '''
                if masterpaths18.__len__() > 0:
                    print(a.origin + "," + a.destination + "," + str(rejectCount) + "," + str(masterpaths18.__len__())
                      + "," + str(rejectCount / masterpaths18.__len__()))
                    '''
    return masterList


def regionTimePeriodPathCountAnalysis(regions17: list, regions18: list, amLow: str, amHigh: str, pmLow: str, pmHigh: str):
    """
    :param regions17: the 2017 regions
    :param regions18: the 2018 regions
    :param amLow: the start of the am period
    :param amHigh: the end of the am period
    :param pmLow: the start of the pm period
    :param pmHigh: the end of the pm period
    :return: a list of lists containing the origin, destination,
    time period (morning or afternoon), path id,  z score, and p value
    """

    # this is the list of lists to be returned
    masterList = []

    masterList.append(["origin", 'destination', 'period', 'path', 'zscore', 'pvalue'])


    size17 = 0
    for i in regions17:
        size17 += i.getCount()

    size18 = 0
    for i in regions18:
        size18 += i.getCount()

    # create a list of path counts for each year and each time period

    for a in regions17:
        for b in regions18:



            am17Paths = {}
            pm17Paths = {}

            am18Paths = {}
            pm18Paths = {}

            if a.origin == b.origin and a.destination == b.destination:

                rejectCount = 0
                AMRejectCount = 0
                PMRejectCount = 0


                # get all the path counts from 17
                times = a.getTimes()
                am = am17Paths
                pm = pm17Paths
                for t in times:

                    timeNode = times[t]
                    time = timeNode.getTimeID()
                    paths = timeNode.getPaths()

                    # if am
                    if timeToInt(time) > timeToInt(amLow) and timeToInt(time) < timeToInt(amHigh):
                        for p in paths:

                            # if we have already seen this path
                            if am.__contains__(p):
                                masterPath = am[p]
                                path = paths[p]
                                masterPath.setCount(masterPath.getCount() + path.getCount())

                            # if we have not seen this path
                            else:
                                am[p] = paths[p]
                    # if pm
                    if timeToInt(time) > timeToInt(pmLow) and timeToInt(time) < timeToInt(pmHigh):
                        for p in paths:

                            # if we have already seen this path
                            if pm.__contains__(p):
                                masterPath = pm[p]
                                path = paths[p]
                                masterPath.setCount(masterPath.getCount() + path.getCount())

                            # if we have not seen this path
                            else:
                                pm[p] = paths[p]

                # get all the path counts from 18
                times = b.getTimes()
                am = am18Paths
                pm = pm18Paths

                for t in times:

                    timeNode = times[t]
                    time = timeNode.getTimeID()
                    paths = timeNode.getPaths()

                    # if am
                    if timeToInt(time) > timeToInt(amLow) and timeToInt(time) < timeToInt(amHigh):
                        for p in paths:

                            # if we have already seen this path
                            if am.__contains__(p):
                                masterPath = am[p]
                                path = paths[p]
                                masterPath.setCount(masterPath.getCount() + path.getCount())

                            # if we have not seen this path
                            else:
                                am[p] = paths[p]
                    # if pm
                    if timeToInt(time) > timeToInt(pmLow) and timeToInt(time) < timeToInt(pmHigh):
                        for p in paths:

                            # if we have already seen this path
                            if pm.__contains__(p):
                                masterPath = pm[p]
                                path = paths[p]
                                masterPath.setCount(masterPath.getCount() + path.getCount())

                            # if we have not seen this path
                            else:
                                pm[p] = paths[p]



                # make it so each path list contains all the same paths (am to am and pm to pm)
                # make it so each list of paths contains the same paths
                for e in am17Paths:
                    if am18Paths.__contains__(e) is False:
                        am18Paths[e] = PathNode.PathNode(e)
                for f in am18Paths:
                    if am17Paths.__contains__(f) is False:
                        am17Paths[f] = PathNode.PathNode(f)

                for e in pm17Paths:
                    if pm18Paths.__contains__(e) is False:
                        pm18Paths[e] = PathNode.PathNode(e)
                for f in pm18Paths:
                    if pm17Paths.__contains__(f) is False:
                        pm17Paths[f] = PathNode.PathNode(f)

                # am analysis
                for p in am17Paths:
                    pathNode17 = am17Paths[p]
                    pathNode18 = am18Paths[p]
                    zscore, pvalue = two_proprotions_test(pathNode17.getCount(), a.getCount(),
                                                          pathNode18.getCount(), b.getCount())
                    smallList = [a.origin, a.destination, "AM", p, zscore, pvalue]
                    masterList.append(smallList)

                    if pvalue <= 0.05:
                        rejectCount += 1
                        AMRejectCount += 1

                # pm analysis
                for p in pm17Paths:
                    pathNode17 = pm17Paths[p]
                    pathNode18 = pm18Paths[p]
                    zscore, pvalue = two_proprotions_test(pathNode17.getCount(), a.getCount(),
                                                          pathNode18.getCount(), b.getCount())
                    smallList = [a.origin, a.destination, "PM", p, zscore, pvalue]
                    masterList.append(smallList)

                    if pvalue <= 0.05:
                        rejectCount += 1
                        PMRejectCount += 1

                if pm17Paths.__len__() > 0 and am17Paths.__len__() > 0:
                    print(amLow + "," + a.origin + "," + a.destination + "," + str(AMRejectCount / am17Paths.__len__())
                          + "," + str(PMRejectCount / pm17Paths.__len__()))

    return masterList


def main():

    sys.argv.pop(0)
    inputFile17 = sys.argv.pop(0)
    inputFile18 = sys.argv.pop(0)

    # create the od nodes
    ODNodes17 = getODNodesFromFile(inputFile17, 30)
    ODNodes18 = getODNodesFromFile(inputFile18, 30)

    # create the regions
    regions17 = setUpRegions(ODNodes17)
    regions17 = filterPaths(regions17)
    regions18 = setUpRegions(ODNodes18)
    regions18 = filterPaths(regions18)


    # analyze the region count
    regionalCountAnalysis = regionCountAnalysis(regions17, regions18)
    with open("STATregionalCountAnalysis.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(regionalCountAnalysis)
    file.close()

    # analyze the path counts
    # year to year
    pathCounts = pathCountAnalysis(regions17, regions18)
    with open("STATPathCountAnalysis.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(pathCounts)
    file.close()

    # relative to od region
    regionPathAnalysis = regionPathCountAnalysis(regions17, regions18)
    with open("STATRegionPathCountAnalysis.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(regionPathAnalysis)
    file.close()

    # relative to od region and morning and afternoon
    regionTimePeriodPath = regionTimePeriodPathCountAnalysis(regions17, regions18, "00:00", "12:00", "12:00", "23:59")
    with open("STATRegionTimePeriodPathCountAnalysis-total.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(regionTimePeriodPath)
    file.close()
    regionTimePeriodPath = regionTimePeriodPathCountAnalysis(regions17, regions18, "05:30", "09:30", "15:00", "17:00")
    with open("STATRegionTimePeriodPathCountAnalysis-tollingHours.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(regionTimePeriodPath)
    file.close()

    # relative to od region and thirty min time interval
    completePathAnalysis = completePathCountAnalysis(regions17, regions18)
    with open("STATCompletePathAnalysis.csv", 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(completePathAnalysis)
    file.close()

    print("Done.")


main()

# end of file
