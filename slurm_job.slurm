#!/bin/bash
#SBATCH --account=lp_h_ds_students
#SBATCH --cluster=genius
#SBATCH --cpus-per-task=1
#SBATCH --job-name=benchmark_tstree
#SBATCH --output=logs/benchmark_output_%j.log
#SBATCH --error=logs/benchmark_error_%j.log
#SBATCH --ntasks=1
#SBATCH --time=00:15:00
#SBATCH --mem=4G
#SBATCH --cpus-per-task=1

# Load modules if necessary
# module load python/3.10

# source ~/envs/myenv/bin/activate

# Run benchmark
python3 benchmark/benchmark.py
