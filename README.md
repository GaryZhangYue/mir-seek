## Introduction
mir-seek is a highly reproducible pipeline to analyze miRNA sequencing data. It takes raw single-end Illumina reads, trims them with Trimmomatics, and counts miRNA reads with miRDeep2. The count table of each sample is merged and collapsed to the mature miRNA level. The pipeline is written in Snakemake to make the pipeline highly reproducible and easily scalable.

## Required pre-installed tools:
1. Trimmomatic 0.38
2. miRDeep2 2.0.1.1
3. Bowtie 1.2.2

The tools above need to be pre-installed with their path exported. Biowulf users only need to install miRDeep2 2.0.1.1 (https://github.com/rajewsky-lab/mirdeep2/releases) as other tools are available as modules and loaded automatically along pipeline processing.
The preprocessed reference files are available elsewhere. Therefore, they need to be placed in /database directory within the cloned repo in local. The pipeline currently only analyzes human miRNA reads; the function of analyzing miRNA reads originating from other organisms will be available in future.

## Steps to initiate the pipeline:
1. Clone the repo to local 
```
git clone git@github.com:GaryZhangYue/mir-seek.git)
```
3. Copy the preprocessed references files to /database directory within the local mir-seek directory
4. Purge and load required modules
```
module purge
module load singularity snakemake python
```
4. Initiate run
```
/your/path/to/mir-seek/mir-seek.py /absolute/path/to/input/data/directory /absolute/path/to/output/directory
```
5. Other functionalities:

      a. --unlock: unlock the directory
      b. –dry-run: perform a dry run
```
/your/path/to/mir-seek/mir-seek.py /absolute/path/to/input/data/directory /absolute/path/to/output/directory --unlock 

/your/path/to/mir-seek/mir-seek.py /absolute/path/to/input/data/directory /absolute/path/to/output/directory --dry-run 
```

## Major output:
Trimming will be done using Trimmomatic. Adapters will be clipped, and low-quality reads will be removed. All remaining reads will be trimmed to 27 bps long, and reads with read length < 18 will be filtered out. The trimmed reads are placed in the directory /Trimmed
miRDeep2 is used to count reads mapped to miRNA database. The miRDeep2 output is placed in the directory mirdeep2/. The merged collapsed mature miRNA count table is mirdeep2/mirdeep2_counts_merged.csv, which is ready for downstream analysis, such as Qiagen IPA and differential expression analysis.
