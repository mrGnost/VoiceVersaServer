#! /bin/bash
#SBATCH --job-name="stargan_train_default"
#SBATCH --gpus=1
#SBATCH --time=0-0:5
#SBATCH --mail-user=damenschikov@edu.hse.ru
#SBATCH --mail-type=ALL
#SBATCH --output="runs/"%j.out
#SBATCH --error="runs/"%j.out
module load CUDA/11.4
module load Python/Anaconda_v11.2021
source activate stargan_py

# Executable
python3 inference.py 415762b7-cd5b-4f54-955b-5c178ebb75a9.wav 230
