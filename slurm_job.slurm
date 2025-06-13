#!/bin/bash
#SBATCH --account=lp_h_ds_students
#SBATCH --cluster=genius
#SBATCH --cpus-per-task=1
#SBATCH --job-name=benchmark_tstree
#SBATCH --output=logs/benchmark_output_%j.log
#SBATCH --error=logs/benchmark_error_%j.log
#SBATCH --ntasks=1
#SBATCH --time=02:00:00
#SBATCH --mem=1G


# Run benchmark
python3 benchmark/benchmark.py