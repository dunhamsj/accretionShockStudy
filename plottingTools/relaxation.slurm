#!/bin/bash

#SBATCH --mail-user=samuel.j.dunham@vanderbilt.edu
#SBATCH --mail-type=END
#SBATCH --nodes=1
#SBATCH --time=0-01:00:00
#SBATCH --mem=128G
#SBATCH --output=relax.%j.out
#SBATCH --job-name=relax

module restore DataAnalysis
source /home/dunhamsj/dataAnalysis/bin/activate

python3 relaxation.py
