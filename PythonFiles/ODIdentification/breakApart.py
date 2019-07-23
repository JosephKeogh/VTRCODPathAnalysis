import csv

for d in range(0, 5):

    originalFileName = "trips" + str(d) + ".csv"

    '''needs to be outside of file loop'''
    '''need to have separate smaller files for each of larger trip files'''
    fileCount = 0

    with open(originalFileName, 'r', newline='') as original:

        print("Reading file: " + originalFileName)

        reader = csv.reader(original)

        '''the line count for this smaller file'''
        lineCount = 0

        for line in reader:

            if lineCount % 100000 == 0:
                fileCount += 1
                lineCount = 0
                print("writing to file: " + str(fileCount))

            fileName = "smaller-" + str(fileCount) + ".csv"
            with open(fileName, 'a', newline='') as smaller:
                writer = csv.writer(smaller)
                writer.writerow(line)

            lineCount += 1

    original.close()

# end of file
