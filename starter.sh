#!/bin/bash
#SBATCH --nodes=1                    # 1 node
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=28
#SBATCH --mem=100000MB          
#SBATCH --time=23:00:00               
#SBATCH --output=hello-%j.out
#SBATCH --error=hello-%j.err

which python
cd /home/kaurov/data/lab/kaurov/misha/MDPL2/snapshot_${snap_id}
echo $pdf_c1
echo $pdf_c2
echo $snap_id
python MDPL2_small_spheres.py ${pdf_c1} ${pdf_c2} ${snap_id}
