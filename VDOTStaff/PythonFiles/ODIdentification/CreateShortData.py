import csv

# open the data file
data = []
with open("trips.csv", "r", newline='') as inputFile:
    inputData = csv.reader(inputFile)
    print('finished reading input file')

    count = 0
    for inputLine in inputData:
        data.append(inputLine)
        count = count + 1
        if count >= 1000:
            break

inputFile.close()

# write the short data into file
with open("ShortDataTrip0.csv", 'w', newline='') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerows(data)
csvFile.close()

print('done')





