#!/bin/bash

# copy the script that breaks apart the large files into smaller ones
cp breakApart.sh /newscratch/jgk7uf/Everything-17
cp breakApart.sh /newscratch/jgk7uf/Everything-18

# copy the set up files
cp setUp.sh /newscratch/jgk7uf/Everything-17
cp setUp.sh /newscratch/jgk7uf/Everything-18

# copy the clean up files
cp cleanUp.sh /newscratch/jgk7uf/Everything-17
cp cleanUp.sh /newscratch/jgk7uf/Everything-18

# copy the slurm request
cp request17.slurm /newscratch/jgk7uf/Everything-17
cp request18.slurm /newscratch/jgk7uf/Everything-18

# copy the super main shell program
cp SuperMain17.sh /newscratch/jgk7uf/Everything-17
cp SuperMain18.sh /newscratch/jgk7uf/Everything-18

# copy the date time file
cp utc2017AllDay.csv /newscratch/jgk7uf/Everything-17
cp utc2018AllDay.csv /newscratch/jgk7uf/Everything-18

# copy the trips files
cp tripsDetected.csv /newscratch/jgk7uf/Everything-17
cp tripsDetected.csv /newscratch/jgk7uf/Everything-18
cp 'tripsDetected (1).csv' /newscratch/jgk7uf/Everything-17
cp 'tripsDetected (1).csv' /newscratch/jgk7uf/Everything-18

# copy the objects
cp -a Objects /newscratch/jgk7uf/Everything-17
cp -a Objects /newscratch/jgk7uf/Everything-18

# copy Main.py
cp Main.py /newscratch/jgk7uf/Everything-17
cp Main.py /newscratch/jgk7uf/Everything-18

# copy the combine program
cp Combine.py /newscratch/jgk7uf/Everything-17
cp Combine.py /newscratch/jgk7uf/Everything-18

# copy the analyzer
cp AnalyzeOutput.py /newscratch/jgk7uf/Everything-17
cp AnalyzeOutput.py /newscratch/jgk7uf/Everything-18

# copy slurm script to combine
cp combine17.slurm /newscratch/jgk7uf/Everything-17
cp combine18.slurm /newscratch/jgk7uf/Everything-18

# copy slurm script to analyze
cp analyze17.slurm /newscratch/jgk7uf/Everything-17
cp analyze18.slurm /newscratch/jgk7uf/Everything-18



