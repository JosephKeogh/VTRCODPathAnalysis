#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=12:00:00
#SBATCH --partition=standard
#SBATCH --account=rivanna-vtrc

# this is the file that will request the job

# set up the environment
module purge
module load anaconda

python AnalyzeOutput.py finalOutput2018.txt analysis2018.txt
mv PathCounts.csv PathCounts2018.csv
python TableauInput.py finalOutput2018.txt TableauInput2018.csv