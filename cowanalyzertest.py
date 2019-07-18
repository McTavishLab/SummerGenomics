# changing file format from vcf to fasta
# input: vcf file name
# output: original vcf file as fasta
# need to get to work without specific file name
import sys
import os
bos_file = "simulated_data_mctavish_lab.vcf"
base = os.path.splitext(bos_file)[0]
os.rename(bos_file, base + ".fasta")

# function designed to replace o with ref and 1 with alt
def cow_analysis(basepair):
    for line in readlines()[6:]:
    # assumes all files have 6 introductory lines to be skipped
        #if 0:
            #str.replace(0, ???)
# stuck here!! )-;  
