#!/bin/bash

# copy the script that breaks apart the large files into smaller ones
cp breakApart.sh /scratch/jgk7uf/Everything-17
cp breakApart.sh /scratch/jgk7uf/Everything-18

# copy the set up files
cp setUp.sh /scratch/jgk7uf/Everything-17
cp setUp.sh /scratch/jgk7uf/Everything-18

# copy the clean up files
cp cleanUp.sh /scratch/jgk7uf/Everything-17
cp cleanUp.sh /scratch/jgk7uf/Everything-18

# copy the slurm request
cp request17.slurm /scratch/jgk7uf/Everything-17
cp request18.slurm /scratch/jgk7uf/Everything-18

# copy the super main shell program
cp SuperMain17.sh /scratch/jgk7uf/Everything-17
cp SuperMain18.sh /scratch/jgk7uf/Everything-18

# copy the date time file
cp utc2017AllDay.csv /scratch/jgk7uf/Everything-17
cp utc2018AllDay.csv /scratch/jgk7uf/Everything-18

# copy the trips files
cp tripsDetected.csv /scratch/jgk7uf/Everything-17
cp tripsDetected.csv /scratch/jgk7uf/Everything-18
cp 'tripsDetected (1).csv' /scratch/jgk7uf/Everything-17
cp 'tripsDetected (1).csv' /scratch/jgk7uf/Everything-18

# copy the objects
cp -a Objects /scratch/jgk7uf/Everything-17
cp -a Objects /scratch/jgk7uf/Everything-18

# copy Main.py
cp Main.py /scratch/jgk7uf/Everything-17
cp Main.py /scratch/jgk7uf/Everything-18

# copy the combine program
cp Combine.py /scratch/jgk7uf/Everything-17
cp Combine.py /scratch/jgk7uf/Everything-18

# copy the analyzer
cp AnalyzeOutput.py /scratch/jgk7uf/Everything-17
cp AnalyzeOutput.py /scratch/jgk7uf/Everything-18

# copy slurm script to combine
cp combine17.slurm /scratch/jgk7uf/Everything-17
cp combine18.slurm /scratch/jgk7uf/Everything-18

# copy slurm script to analyze
cp analyze17.slurm /scratch/jgk7uf/Everything-17
cp analyze18.slurm /scratch/jgk7uf/Everything-18



