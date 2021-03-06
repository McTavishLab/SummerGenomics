# changing file format from vcf to fasta
# input: vcf file name
# output: original vcf file as fasta
# need to get to work without specific file name
import sys
import os
import random
import gzip

cutoff = 6000000

bos_file = sys.argv[1]
#"simulated_data_mctavish_lab.vcf"

base = os.path.splitext(bos_file)[0]
outfile_name = base + ".fasta"
outfile = open(outfile_name, "w")

#Skip mitochondrial information
mito_tag = "NC_006853.1"
sep = "/"

def vcf_call_to_bases(ref, alt, call):
    geno = call.replace('0', ref).replace('1',alt)
    #todo: handle ./.?
    return geno


def random_base(geno):
    index = random.randint(1,2)
    if index == 1:
         return geno[0]
    elif index == 2:
        return geno[2]
    else:
        print("ERRROORRRR")


index_dict = {}
sequence_dict = {}


infi = gzip.open(bos_file,"r")
counter = 0
for line in infi.readlines():
    counter += 1
    if(counter >= cutoff):
        break
#    print("line {}".format(counter))
    if line.startswith('##'):
        pass
    elif line.startswith('#'):
        headers = line.split()
        print(headers)
        for i, val in enumerate(headers):
            index_dict[i]=val
    else:
        if ".%s." % (sep) in line:
            continue
        elif mito_tag in line:
            continue
        vcfrow = line.split()
        for ii in range(9,len(vcfrow)):
            sample_name = index_dict[ii]
            if sample_name not in sequence_dict:
                sequence_dict[sample_name] = ''
            geno_call = vcf_call_to_bases(vcfrow[3], vcfrow[4], vcfrow[ii].split(":")[0])
            base_call = random_base(geno_call)
            added_seq = sequence_dict[sample_name] + base_call
            sequence_dict[sample_name] = added_seq
    if(counter % 10000==0):
        print(counter)
infi.close()

#See sequence for each sample
#for key in sequence_dict:
#     print("name {}, sequence {}".format(key, sequence_dict[key]))

#Write out sequences to fasta file
for key in sequence_dict:
  outline = ">%s\n%s\n" % (key,sequence_dict[key])
  outfile.write(outline)

outfile.close()


'''
base = os.path.splitext(bos_file)[0]
os.rename(bos_file, base + ".fasta")

# function designed to replace o with ref and 1 with alt
def cow_analysis(basepair):
    for line in readlines()[6:]:
    # assumes all files have 6 introductory lines to be skipped
        #if 0:
            #str.replace(0, ???)
# stuck here!! )-;  
'''
