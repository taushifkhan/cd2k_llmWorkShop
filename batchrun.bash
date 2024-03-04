#!/bin/bash
#SBATCH --job-name=openAI_response
#SBATCH --output=run_g4.out
#SBATCH -n 1
#SBATCH --cpus-per-task=4
#SBATCH --time=24:00:00
#SBATCH --mem=30G
#SBATCH --mail-user=taushif.khan@jax.org
#SBATCH --mail-type=ALL

source /home/${USER}/.bashrc
conda activate openAIFunc 

python openAI_api_v1.1.py -p ./param/ifn_workshop.json -g ./data/M8.3_geneList.csv -o ./outResults_g4/M8.3_response1_g4.json

python openAI_api_v1.1.py -p ./param/ifn_workshop.json -g ./data/M10.1_geneList.csv -o ./outResults_g4/M10.1_response1_g4.json
python openAI_api_v1.1.py -p ./param/ifn_workshop.json -g ./data/M13.17_geneList.csv -o ./outResults_g4/M13.17_response1_g4.json
python openAI_api_v1.1.py -p ./param/ifn_workshop.json -g ./data/M15.86_geneList.csv -o ./outResults_g4/M15.86_response1_g4.json
python openAI_api_v1.1.py -p ./param/ifn_workshop.json -g ./data/M15.127_geneList.csv -o ./outResults_g4/M15.127_response1_g4.json
