import csv

fileCount = 0

for d in range(0, 5):

    originalFileName = "trips" + str(d) + ".csv"

    '''needs to be outside of file loop'''
    '''need to have separate smaller files for each of larger trip files'''

    with open(originalFileName, 'r', newline='') as original:

        print("Reading file: " + originalFileName)

        reader = csv.reader(original)

        '''the line count for this smaller file'''
        lineCount = 0

        '''keep track of the lines to write to the smaller file'''
        lines = []

        for line in reader:

            if line.__len__() >= 11:
                lines.append(line)
            lineCount += 1

            if lineCount % 100000 == 0:

                fileName = "smaller-" + str(fileCount) + ".csv"
                print("writing to file: " + fileName)
                with open(fileName, 'w', newline='') as smaller:
                    writer = csv.writer(smaller)
                    writer.writerows(lines)
                smaller.close()

                '''reset'''
                fileCount += 1
                lineCount = 0
                lines = []


    original.close()

# end of file
