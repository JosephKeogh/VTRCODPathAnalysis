#!/bin/bash

# variables moving forward
printProgress=true
testPerformance=false

# analyze the data
# $1 is the iteration, this is passed in by request.slurm
python Main.py smaller- utc2018AllDay.csv totalOutput2018 $printProgress $testPerformance $1


