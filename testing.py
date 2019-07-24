import csv

with open("smaller-074.csv", 'r', newline='') as f:

    reader = csv.reader(f)

    count = 0

    for line in reader:

        count += 1

        l = line.__len__()

        if l < 11:
            print(count)
            print(line)
f.close()