#!/bin/bash
#SBATCH -J ANCHOR # Job name
#SBATCH -o ANCHOR.o # Name of Output File
#SBATCH -e ANCHOR.e # Name of Error File
#SBATCH --time=24:00:00                                         
#SBATCH --qos=huge-long                                          
#SBATCH --mem=128gb
#SBATCH --partition=cbcb
#SBATCH --account=cbcb
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=32
#SBATCH --mail-user=hsmurali@terpmail.umd.edu # Email for job info
#SBATCH --mail-type=ALL # Get email for begin, end, and fail

module load conda
source activate binnacle_env
python ANCHOR.py 