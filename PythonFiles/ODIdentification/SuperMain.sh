#!/bin/bash

# initialize the environment
module purge
module load anaconda

# variables moving forward
printProgress=true
testPerformance=false

# the iteration we are on
iteration=$1

# analyze the data
# the 0 at the end will become $iteration
python Main.py trips utc2017AllDay.csv AllXDInfo-17.csv totalOutputTest $printProgress $testPerformance 0

# view the output of the analysis
# more totalOutputTest.txt
