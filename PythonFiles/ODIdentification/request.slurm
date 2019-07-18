!#/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=12:00:00
#SBATCH --partition=standard
#SBATCH --account=rivanna-vtrc

# this is the file that will request the job

# run the shell file that executes the program
./SuperMain.sh
