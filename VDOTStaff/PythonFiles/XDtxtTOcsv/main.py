# this file will be used to take XD data that is from a txt file, and put it into a csv file
# the csv file must be in the proper format
# this program must be able to handle multiple files being passed to it

# imports
import csv

# functions
def fileToArray(fileName):

    # open text file
    file = open(fileName, 'r')

    # read out the first line of the file
    file.readline()

    fileArray = []

    # read the file line by line
    for line in file:
        # take out white space
        line.strip(" ")
        # make the line an array of strings
        lineArray = line.split(",")

        # add the line to an array
        fileArray.append(lineArray)

    return fileArray

#only gives us what we want from the data
def trimArray(arr, corridor, period):

    cleanArray = []

    for data in arr:
        # take out what we don't need from the line
        neededData = [data[2], data[13], corridor, period]
        cleanArray.append(neededData)

    return cleanArray

# these functions take in an array of arrays, and sort the array so that it is in the order a driver would travel
# it is based on lat and longitude values
def sortHeadNorth(arr):
    # smallest lat first
    arr.sort(key = sortLat)
    return

def sortHeadSouth(arr):
    # largest lat first
    arr.sort(key=sortLat, reverse=True)
    return

def sortHeadWest(arr):
    # largest long first
    arr.sort(key=sortLong, reverse=True)
    return

def sortHeadEast(arr):
    # smallest long first
    arr.sort(key=sortLong)
    return

def sortLat(arr):
    return arr[17]
def sortLong(arr):
    return arr[20]

def massiveMethod(fileName, corridor, period, direction):

    # put the file into the array
    fileArray = fileToArray(fileName)

    # order the array based on how it would be traveled
    if(direction == "North"):
        sortHeadNorth(fileArray)
    if(direction == "South"):
        sortHeadSouth(fileArray)
    if (direction == "West"):
        sortHeadWest(fileArray)
    if (direction == "East"):
        sortHeadEast(fileArray)

    # trim the data
    cleanArray = trimArray(fileArray, corridor, period)

    # add the order values to the arrays
    count = 1
    for data in cleanArray:
        data.append(count)
        count = count + 1

    return cleanArray


def addData(arr1, arr2):

    for line in arr1:
        arr2.append(line)

    return

# main method
I495N = massiveMethod("rest17.txt", "GWPKWY-N-495-S-7-S-I66-W", "PM", "South")

totalArray = []

addData(I495N, totalArray)

# open the csv file
with open("rest17.csv", 'w', newline='') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerows(totalArray)

csvFile.close()

print("Done.")

