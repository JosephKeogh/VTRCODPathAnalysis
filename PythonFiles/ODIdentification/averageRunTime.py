
totalTime = 0
runs = 0
with open("runs.txt", 'r', newline='') as file:
    for line in file:
        line = line.strip()
        totalTime = totalTime + float(line)
        runs += 1
file.close()

print("Runs: " + str(runs))

average = totalTime / runs
print("1000 Lines Average:  " + str(average)[0:5] + " sec")

# how long it will take to run the entire program (analyze all files)
estimateSec = average * (10000000 / 1000) * 2
estimateH = estimateSec / 60 / 60
print("Estimated Run Time: " + str(estimateH)[0:5] + "  hr")
# end of file
