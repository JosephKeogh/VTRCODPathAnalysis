import csv
import sys

sys.argv.pop(0)

with open(sys.argv.pop(0), 'r', newline='') as f:

    reader = csv.reader(f)

    count = 0

    for line in reader:

        count += 1

        l = line.__len__()

        if l < 11:
            print(count)
            print(line)
f.close()