#!/bin/bash

#SBATCH --mail-user=samuel.j.dunham@vanderbilt.edu
#SBATCH --mail-type=END
#SBATCH --nodes=1
#SBATCH --time=1-00:00:00
#SBATCH --mem=128G
#SBATCH --output=mm1D.%j.out
#SBATCH --job-name=mm1D

module restore DataAnalysis
source /home/dunhamsj/dataAnalysis/bin/activate

python3 makeMovie1D.py
