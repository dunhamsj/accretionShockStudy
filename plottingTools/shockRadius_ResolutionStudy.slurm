#!/bin/bash

#SBATCH --mail-user=samuel.j.dunham@vanderbilt.edu
#SBATCH --mail-type=END,FAIL
#SBATCH --nodes=1
#SBATCH --time=1-00:00:00
#SBATCH --mem=128G
#SBATCH --output=sr.%j.out
#SBATCH --job-name=sr

module restore DataAnalysis
source /home/dunhamsj/dataAnalysis/bin/activate

python3 shockRadius_ResolutionStudy.py
