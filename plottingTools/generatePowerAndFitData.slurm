#!/bin/bash

#SBATCH --mail-user=samuel.j.dunham@vanderbilt.edu
#SBATCH --mail-type=END,FAIL
#SBATCH --nodes=1
#SBATCH --time=0-10:00:00
#SBATCH --mem=128G
#SBATCH --output=gPower.%j.out
#SBATCH --job-name=genPower

module restore DataAnalysis
source /home/dunhamsj/dataAnalysis/bin/activate

python3 -u generatePowerAndFitData.py
