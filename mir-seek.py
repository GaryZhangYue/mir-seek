#!/usr/bin/env python3

import argparse
import os
import shutil
import subprocess
import json

__author__   = 'Yue (Gary) Zhang, Ph.D'
__email__    = 'zhangy68@nih.gov'
_description = 'A pipeline to quantify miRNA copies from single-end illumina raw reads'


# Define command-line arguments
parser = argparse.ArgumentParser(description="Specify rawdata and output directories")
parser.add_argument("input_dir", help="Path to input directory")
parser.add_argument("output_dir", help="Path to output directory")
parser.add_argument("-d", "--dry-run", action="store_true", help="Perform a dry run")
parser.add_argument("-u", "--unlock", action="store_true", help="Unlock the working directory")
args = parser.parse_args()


# Define working directory as current directory
work_dir = os.getcwd()

# Copy config, workflow, and database directories to working directory
script_dir = os.path.dirname(os.path.abspath(__file__))
for dir_name in ["config", "workflow", "database"]:
    source_dir = os.path.join(script_dir, dir_name)
    dest_dir = os.path.join(work_dir, dir_name)
    if os.path.exists(source_dir) and not os.path.exists(dest_dir):
        shutil.copytree(source_dir, dest_dir)

# Build config dictionary with input and output directory paths
config = {
        "path_raw_reads": args.input_dir, 
        "path_analysis": args.output_dir,
        "path_root": work_dir,
        "references":
             {
             "adapters": os.path.join(work_dir,"database/TruSeq_and_nextera_adapters_20210423.fa"),
             "hg38_index": os.path.join(work_dir,"database/hg38_genome_processed_bowtie_index"),
             "hg38_fasta": os.path.join(work_dir, "database/Homo_sapiens_assembly38_whitespace_removed_asterisk_tab_replaced_probLet_removed.fasta"), 
             "mature": os.path.join(work_dir, "database/mature.fa"),
             "hairpin": os.path.join(work_dir,"database/hairpin_probLet_removed.fa")
             }
         }
# Concatenate all .json files in config directory into config.json
for file in os.listdir(os.path.join(work_dir, "config")):
    if file in ['cluster.json', 'modules.json']:
        with open(os.path.join(work_dir, "config", file)) as f:
            config.update(json.load(f))
with open(os.path.join(work_dir, "config.json"), "w") as f:
    json.dump(config, f)

# Set path to Snakefile
snakefile = os.path.join(work_dir, "workflow", "Snakefile")

# Pass cluster specification to Snakemake
if os.path.exists(os.path.join(work_dir, "config", "cluster.json")):
    cluster_file = os.path.join(work_dir, "config", "cluster.json")
    cmd = f"snakemake --directory {args.output_dir} --snakefile {snakefile} --configfile {os.path.join(work_dir, 'config.json')} --use-envmodules --rerun-incomplete --cores all --cluster-config {cluster_file}"
    cmd += " --cluster 'sbatch --gres {cluster.gres} --cpus-per-task {cluster.threads} -t {cluster.time} --mem {cluster.mem} --job-name={params.rname}' -j 500"
else:
    cmd = f"snakemake --directory {args.output_dir} --snakefile {snakefile} --configfile {os.path.join(work_dir, 'config.json')} --use-envmodules --rerun-incomplete --cores all"
print(cmd)
# Add dry-run and unlock options
if args.dry_run:
    cmd += " --dryrun"
if args.unlock:
    cmd += " --unlock"
# Run snakemake
subprocess.call(cmd, shell=True)



