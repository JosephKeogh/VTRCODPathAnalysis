!#/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=12:00:00
#SBATCH --partition=standard
#SBATCH --account=rivanna-vtrc

# this is the file that will request the job

# set up the environment
module purge
module load anaconda

# clear the output files
python ClearOutput.py

# run the shell file that executes the program
# pass the run number (array number)
./SuperMain.sh ${SLURM_ARRAY_TASK_ID}
