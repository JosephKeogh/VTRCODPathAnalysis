import csv
import sys
from datetime import datetime
from Objects import Coordinate, ODNode, TimeNode, PathNode


'''functions'''
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

'''get arguments'''
sys.argv.pop(0)
inputFileName = sys.argv.pop(0)
outputFileName = sys.argv.pop(0)

"""the running counts"""
totalAM = 0
totalPM = 0
totalCountFromNodes = 0

"""the marker between morning and afternoon"""
noonTime = "12:00"
noon = timeToInt(noonTime)

'''list of od nodes'''
ODNodes = []

with open(inputFileName, 'r') as outputTextFile1:

    for line in outputTextFile1:
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
            voriginLine = outputTextFile1.readline().strip()
            if voriginLine == '':
                break

            vorigin = voriginLine[8:]
            vcommaIndex = vorigin.index(",")
            voriginLat = vorigin[:vcommaIndex]
            voriginLong = vorigin[vcommaIndex + 1:]
            voriginC = Coordinate.Coordinate(float(voriginLat), float(voriginLong))

            '''get the destination of the od node'''
            vdestLine = outputTextFile1.readline().strip()
            vdestination = vdestLine[13:]
            vcommaIndex = vdestination.index(",")
            vdestlat = vdestination[:vcommaIndex]
            vdestlong = vdestination[vcommaIndex + 1:]
            vdestC = Coordinate.Coordinate(float(vdestlat), float(vdestlong))

            '''get the count of the od node'''
            vcountLine = outputTextFile1.readline().strip()
            vcount = vcountLine[7:]

            '''get the am count of the od node'''
            vamCountLine = outputTextFile1.readline().strip()
            vamCount = vamCountLine[9:]

            '''get the pm count of the od node'''
            vpmCountLine = outputTextFile1.readline().strip()
            vpmCount = vpmCountLine[9:]

            '''increment the global time period totals'''
            totalAM += int(vamCount)
            totalPM += int(vpmCount)

            '''create the od node'''
            vodnode = ODNode.ODNode(voriginC, vdestC, int(vcount))

            '''update the period counts of the od node'''
            vodnode.setAmCount(int(vamCount))
            vodnode.setPmCount(int(vpmCount))

            '''readout the "Times: "'''
            readOut = outputTextFile1.readline().strip()

            '''update the times of the od node'''
            vt = outputTextFile1.readline().strip()

            '''for all the timenodes listed'''
            while vt.__contains__("WeekDay"):
                '''get the weekday, time, and count'''
                weekday = int(vt[9:11])
                vtime = vt[19:24]
                vcount = int(vt[32:])

                '''create the TimeNode'''
                vdt = datetime.strptime(vtime, "%H:%M")
                vtimenode = TimeNode.TimeNode(vdt, weekday, 1)
                vtimenode.setCount(vcount)

                '''the dict to be used as the dict of paths for timenode'''
                paths = {}

                '''read the next line in the file'''
                nl = outputTextFile1.readline().strip()

                # changed the output of the hashtable to be correct
                if nl.__contains__("Paths"):

                    nl = outputTextFile1.readline().strip()

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

                        nl = outputTextFile1.readline().strip()

                    vt = nl

                '''set the paths of the time node'''
                vtimenode.setPaths(paths)

                vt = nl
                '''add the time node to the list of times in od node'''
                vodnode.addTimeNode(vtimenode)

            if vt.__contains__("Index"):
                line = vt

            '''add the od node to the list of od nodes'''
            ODNodes.append(vodnode)

outputTextFile1.close()


'''write all the nodes to a csv file'''
with open(outputFileName, 'w', newline='') as output:
    writer = csv.writer(output)

    writer.writerow(["OriginLat", "OriginLong", "DestinationLat", "DestinationLong", "InterestCount%", "AM%", "PM%"])

    for i in ODNodes:

        totalPercent = str(round((i.getCount() / interestTripCount), 4))
        print('Total percent: ' + str(totalPercent))

        if float(totalPercent) > 1:
            print('Total percent: ' + str(totalPercent))
            print('node count: ' + str(i.getCount()))
            print('interest trip count: ' + str(interestTripCount))

        amPercent = str(i.getAmCount() / totalAM)[:5]
        pmPercent = str(i.getPmCount() / totalPM)[:5]

        '''if not a dummy node'''
        writer.writerow([i.origin.lat, i.origin.long, i.destination.lat, i.destination.long,
                             totalPercent, amPercent, pmPercent])

output.close()


# end of file
