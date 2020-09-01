"""A script to create a fasta file of one sample from a vcf"""
import sys
import os
import random
import gzip


# Input file - should be in vcf format, can me .gz or uncompress
bos_file = sys.argv[1]


# If you run with only an input file, will print sample names and exit

# Second argument should be the sample name you want a fasta for
if len(sys.argv) > 2:
    sample_name = sys.argv[2]
else:
    sample_name = None


## Useful for running a quick trial
## Stops after cutoff number of sites
cutoff = 500000
cutoff_on = False


# Skip mitochondrial information
## TODO should be filtered before instead of hard coded here
mito_tag = "NC_006853.1"
sep = "/"

def vcf_call_to_bases(ref, alt, call):
    assert(len(ref)==1), "ref is {}, why not caught as INDEL?????".format(ref)
    geno = call.replace('0', ref).replace('1',alt).replace('.','?')
    #todo: handle ./.?
    return geno

def random_base(geno):
    nucleotides=["A","T","C","G","?"]
    index = random.randint(1,2)
    assert(geno[0] in nucleotides), "geno 0 is {}".format(geno[0])
    assert(geno[2] in nucleotides), "geno 0 is {}".format(geno[2])
    if index == 1:
         return geno[0]
    elif index == 2:
        return geno[2]
    else:
        print("ERRROORRRR")



index_dict = {} # tracks the names of the samples
sequence_dict = {'reference':''} #Stores the data (memory HOG)

print("About to open file")
if 'gz' in bos_file:
	infi = gzip.open(bos_file, 'r')
else:
	infi = open(bos_file, 'r')
#infi = gzip.open(bos_file,"r")
print("Finished open file")

for line in infi:
    if line.startswith('##'):
        pass
    elif line.startswith('#'):
        headers = line.split()
        print(headers)
        for i, val in enumerate(headers):
            index_dict[val]=i
        break
infi.close()

def get_sequence_for_sample(sample_name, bos_file):
    sample_index = index_dict[sample_name]
    sample_sequence = ''
    if 'gz' in bos_file:
        infi = gzip.open(bos_file, 'r')
    else:
        infi = open(bos_file, 'r')
    counter = 0
    outfile = open("{}.fasta".format(sample_name),'w')
    outfile.write("> {}\n".format(sample_name))
    pos = 0
    for line in infi:
        counter += 1
        if(counter >= cutoff and cutoff_on):
            break
        if line.startswith('#'):
            pass
        else:
#        if ".%s." % (sep) in line:
#             print("skipping line {} due to missing data".format(counter))
#             print(line)
#             continue
            if mito_tag in line:
                continue
            elif "INDEL" in line:
    #            print("skipping line {} due to indel".format(counter))
                continue
            vcfrow = line.split()
            assert(len(vcfrow)>4), vcfrow
            ref = vcfrow[3]
            alt = vcfrow[4]
            if len(alt) > 1: #Skips multi allele, or indels
                continue
            pos += 1     
            if sample_name == 'REF':
                base_call = ref
            else:
          #      if(nucleotides.count(vcfrow[3])!=1 or nucleotides.count(vcfrow[4])!=1):
          #          continue
                call = vcfrow[sample_index].split(":")[0]
                assert(len(ref)==1),  ref
                assert(len(alt)==1),  alt
                assert(len(call)== 3), call
                geno_call = vcf_call_to_bases(ref, alt, call)
                assert(len(geno_call)==3),  geno_call
                base_call = random_base(geno_call)
            outfile.write(base_call)
            if(pos % 80 == 0):
                outfile.write('\n')
        if(counter % 10000==0):
            print(counter)
    outfile.write('\n')
    outfile.close()
    infi.close()



if sample_name:
    get_sequence_for_sample(sample_name, bos_file)

