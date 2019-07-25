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

python AnalyzeOutput.py finalOutput2017.txt analysis2017.txt
python TableauInput.py finalOutput2017.txt TableauInput2017.csv