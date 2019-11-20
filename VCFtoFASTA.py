import sys
import os
import random
import gzip



cutoff = 500000
cutoff_on = False

bos_file = sys.argv[1]
name_outfile = sys.argv[2]
if len(sys>=4):
    meta_file = sys.argv[3]
else:
    meta_file = False
#"simulated_data_mctavish_lab.vcf"



#base = os.path.splitext(bos_file)[0]
#outfile_name = base.strip(".vcf") + ".fasta"

#outfile_name ="test.fasta"
outfile = open(name_outfile, "w")



#Skip mitochondrial information
mito_tag = "NC_006853.1"
sep = "/"



def vcf_call_to_bases(ref, alt, call):
    assert(len(ref)==1), "ref is {}, why not caught as INDEL?????".format(ref)
    geno = call.replace('0', ref).replace('1',alt).replace('.','N')
    #todo: handle ./.?
    return geno



def random_base(geno):
    nucleotides=["A","T","C","G","N"]
    index = random.randint(1,2)
    assert(geno[0] in nucleotides), "geno 0 is {}".format(geno[0])
    assert(geno[2] in nucleotides), "geno 0 is {}".format(geno[2])
    if index == 1:
         return geno[0]
    elif index == 2:
        return geno[2]
    else:
        print("ERRROORRRR")





index_dict = {}
sequence_dict = {'reference':''}



#infi = gzip.open(bos_file,"r")

print("About to open file")
infi = open(bos_file, "r")
print("Finished open file")
counter = 0
for line in infi:
    counter += 1
    if(counter >= cutoff and cutoff_on):
        break
    if line.startswith('##'):
        pass
    elif line.startswith('#'):
        headers = line.split()
        print(headers)
        for i, val in enumerate(headers):
            index_dict[i]=val
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
        ref = vcfrow[3]
        alt = vcfrow[4]
        if len(alt) > 1:
            continue
  #      if(nucleotides.count(vcfrow[3])!=1 or nucleotides.count(vcfrow[4])!=1):
  #          continue
        ref_seq = sequence_dict['reference'] + ref
        sequence_dict['reference'] = ref_seq
        for ii in range(9,len(vcfrow)):
            sample_name = index_dict[ii]
            if sample_name not in sequence_dict:
                sequence_dict[sample_name] = ''
            call = vcfrow[ii].split(":")[0]
            assert(len(ref)==1),  ref
            assert(len(alt)==1),  alt
            assert(len(call)== 3), call
            geno_call = vcf_call_to_bases(ref, alt, call)
            assert(len(geno_call)==3),  geno_call
            base_call = random_base(geno_call)
            added_seq = sequence_dict[sample_name] + base_call
            sequence_dict[sample_name] = added_seq
    if(counter % 10000==0):
        print(counter)
infi.close()



#See sequence for each sample

#for key in sequence_dict:

#     print("name {}, sequence {}".format(key, sequence_dict[key]))
if meta_file:
    #Replace key wiht csv names
    samp_name = {}
    f = open(meta_file,'r')
    for aline in f:
        if 'population' in aline:
            continue 
        asplit = aline.split()
        samp_name[asplit[1]]=asplit[0]

    # outline = samp_name
    #Write out sequences to fasta file

    for key in samp_name:
        print key
        outline = ">%s\n%s\n" % (key,sequence_dict[samp_name[key]])
        outfile.write(outline)
else:
    for key in sequence_dict:
        print key
        outline = ">%s\n%s\n" % (key,sequence_dict[key])
        outfile.write(outline)


    outfile.close()
