import csv

for d in range(0, 5):

    originalFileName = "trips" + str(d) + ".csv"

    with open(originalFileName, 'r', newline='') as original:

        reader = csv.reader(original)

        fileCount = 0
        totalLineCount = 0
        lineCount = 0

        for line in reader:

            if lineCount % 100 == 0:
                fileCount += 1
                lineCount = 0

            fileName = "smaller-" + str(fileCount) + ".csv"
            with open(fileName, 'a', newline='') as smaller:
                writer = csv.writer(smaller)
                writer.writerow([lineCount, totalLineCount])
                writer.writerow(line)

            lineCount += 1
            totalLineCount += 1

    original.close()

# end of file
