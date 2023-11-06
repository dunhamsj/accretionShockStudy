#!/bin/bash

#SBATCH --mail-user=samuel.j.dunham@vanderbilt.edu
#SBATCH --mail-type=END
#SBATCH --nodes=1
#SBATCH --time=0-10:00:00
#SBATCH --mem=128G
#SBATCH --output=mm2D.%j.out
#SBATCH --job-name=mm2D

module restore DataAnalysis
source /home/dunhamsj/dataAnalysis/bin/activate

python makeMovie2D_TwoFields.py
