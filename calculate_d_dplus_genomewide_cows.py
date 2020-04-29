import random as rd
import os.path
import argparse
import gzip
import sys

#Only skip over missing data if missing data is part of the sample we want#Calculate D genomewide.
#python pytonName.py -infile /path/to/name.vcf.gz -outfile /path/to/outfile.csv -p1 cow_cow -p2 cow_monkey -p3 cow_bison -p4 cow_human -meta meta.csv
#make sure meta file has correct individual names and that population names don't include spaces

parser = argparse.ArgumentParser(description="Calulate D genomewide.")

parser.add_argument('-infile',action="store",dest="infile")
parser.add_argument('-outfile',action="store",dest="outfile")
parser.add_argument('-p1',action="store",dest="p1")
parser.add_argument('-p2',action="store",dest="p2")
parser.add_argument('-p3',action="store",dest="p3")
parser.add_argument('-p4',action="store",dest="p4")
parser.add_argument('-meta',action="store",dest="meta_file")

param=parser.parse_args()

def random_geno(genotype,sep):
  geno_list = genotype.split(sep)
  geno = rd.sample(geno_list,1)[0]
  return(geno)

def isAncestral(allele,ancestral):
  return(allele == ancestral)

#Populations to be used
populations = [param.p1,param.p2,param.p3,param.p4] #["bos_taurus","sanga_taurus","bos_indicus","bison_bison"]
pop_name_dicc = {}
with open(param.meta_file,"r") as fp:
  for aline in fp:
    aspline = aline.split()
    pop_name_dicc[aspline[1]]=aspline[0]

#phased or unphased?
sep = "/"

#Mitochondrial tag
mito_tag = "NC_006853.1"

#Open file
file = gzip.open(param.infile,"r")
line = file.readline()

#Define nucleotides
nucleotides = ["A","T","C","G"]

#Get header
while line.startswith('#'):
  header = line.split()
  line = file.readline()

#Get indices for populations to be used
pop_index_dicc = {}
for pop in populations:
  ind = header.index(pop_name_dicc[pop])
  pop_index_dicc[pop] = ind

#Keep count of abba and baba
abba = 0.0;baba = 0.0
#Keep count of baaa and abaa
baaa = 0.0;abaa = 0.0
counter =0.0

#Go through line by line
for line in file:
  counter += 1
  spline = line.split()
  #Do not include mitochondrial data
  if mito_tag in line:
    continue
  #Ignore missing data
  if ".%s." %(sep) in line:
    continue
  #Only biallelic
  if(nucleotides.count(spline[3])!=1 or nucleotides.count(spline[4])!=1):
    continue
  alleles = {}
  pop_count = 1
  for pop in populations:
    if pop == "bos_taurus":
        alleles["pop"+str(pop_count)] = "0"
        pop_count+=1
    else:
        genotype_raw = spline[pop_index_dicc[pop]]
        genotype = genotype_raw.split(':')[0]
        alleles["pop"+str(pop_count)] = random_geno(genotype,sep)
        pop_count+=1

  #Ignore sites where p1 and p2 have same allele
  if(alleles["pop1"] == alleles["pop2"]):
    continue
  #Differentiate between abba/baba and baaa/abaa
  #Is p3 ancestral?
  if(isAncestral(alleles["pop3"],alleles["pop4"])):
    #Is it baaa or abaa:
    if(isAncestral(alleles["pop2"],alleles["pop4"])):
      baaa+=1
    elif(isAncestral(alleles["pop1"],alleles["pop4"])):
      abaa+=1
  #Is it ABBA or BABA
  elif not isAncestral(alleles["pop3"],alleles["pop4"]):
  #ABBA: p1 has ancestral allele
    if(isAncestral(alleles["pop1"],alleles["pop4"])):
      abba += 1
    elif(isAncestral(alleles["pop2"],alleles["pop4"])):
      baba += 1
  if(counter%10000==0):
    print("On line {}. ABBA is {}. BABA is {}.BAAA is {}. ABAA is {}".format(counter,abba,baba,baaa,abaa))
file.close()

#Calculate D
try:
  d = (abba - baba)/(abba + baba)
except ZeroDivisionError:
  d = 'nan'

#Calculate D+
dplus_numerator = (abba - baba) + (baaa - abaa)
dplus_denom = (abba + baba) + (baaa + abaa)
try:
  dplus = dplus_numerator/dplus_denom
except ZeroDivisionError:
  dplus = 'nan'

#Output results. If outfile already exists, append to it instead of creating outfile again
if(os.path.exists(param.outfile)):
  fout = open(param.outfile,"a+")
  outline = param.p1+"\t"+param.p2+"\t"+param.p3+"\t"+param.p4+"\t"
  outline += str(abba) + "\t" + str(baba) +"\t"+ str(baaa) +"\t"+ str(abaa) +"\t"+ str(d) + "\t"+str(dplus)+"\n"
  fout.write(outline)
  fout.close()
else:
  fout = open(param.outfile,"w")
  outfile_header="p1\tp2\tp3\tp4\tABBA\tBABA\tBAAA\tABAA\tD\tD+\n"
  fout.write(outfile_header)
  outline = param.p1+"\t"+param.p2+"\t"+param.p3+"\t"+param.p4+"\t"
  outline += str(abba) + "\t" + str(baba) +"\t"+ str(baaa) +"\t"+ str(abaa) +"\t"+ str(d)+"\t"+str(dplus)+"\n"
  fout.write(outline)
  fout.close()
