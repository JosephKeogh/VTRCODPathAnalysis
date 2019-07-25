#!/bin/bash
module load anaconda
sbatch --array=0-208 request18.slurm >> r1.txt
job1='python getJobNum.py r1.txt'
rm r1.txt
sbatch --dependency=afterok:${job1} combine18.slurm >> r2.txt
job2='python getJobNum.py r2.txt'
rm r2.txt
sbatch --dependency=afterok:${job2} analyze18.slurm