
import csv

count = 0

with open("smaller-44.csv", 'r', newline='') as f:

    reader = csv.reader(f)

    for line in reader:

        count += 1

        length = line.__len__()

        if length < 5:
            print(count)

            print(line)



f.close()

# end of file
