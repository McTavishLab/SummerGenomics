import random as rd
import argparse
import gzip
import sys
import os

#Calculate D genomewide.
#python pytonName.py -infile /path/to/name.vcf.gz -outfile /path/to/outfile.csv -p1 cow_cow -p2 cow_monkey -p3 cow_bison -p4 cow_human -meta meta.csv
#make sure meta file has correct individual names and that population names don't include spaces

parser = argparse.ArgumentParser(description="Calulate D genomewide.")

parser.add_argument('-infile',action="store",dest="infile")
parser.add_argument('-outfile',action="store",dest="outfile")
parser.add_argument('-p1',action="store",dest="p1")
parser.add_argument('-p2',action="store",dest="p2")
parser.add_argument('-p3',action="store",dest="p3")
parser.add_argument('-p4',action="store",dest="p4")
parser.add_argument('-meta',action="store",dest="meta")

param=parser.parse_args()

def random_geno(genotype,sep):
  geno_list = genotype.split(sep)
  geno = rd.sample(geno_list,1)[0]
  return(geno)

def isAncestral(allele,ancestral):
  return(allele == ancestral)
#File name
infile = param.infile
outfile = param.outfile

#Populations to be used
populations = [param.p1,param.p2,param.p3,param.p4] #["bos_taurus","sanga_taurus","bos_indicus","bison_bison"]
meta_file = param.meta
pop_name_dicc = {}
with open(meta_file,"r") as fp:
  for aline in fp:
    aspline = aline.split()
    pop_name_dicc[aspline[1]]=aspline[0]

#phased or unphased?
sep = "/"

#mitochondrial DNA identifier
mito_tag = "NC_006853.1"

#Open file
file = gzip.open(infile,"r")
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
counter =0.0

#Keep count of abaa and baaa
abaa = 0.0;baaa = 0.0

#Go through line by line
for line in file:
  counter += 1
  spline = line.split()
  #ignore mitochondria DNA
  if mito_tag in line:
    continue
#  #Ignore missing data
#  if ".%s." %(sep) in line:
#    continue
  #Only biallelic
  if(nucleotides.count(spline[3])!=1 or nucleotides.count(spline[4])!=1):
    continue
  alleles = []
  for pop in populations:
    genotype_raw = spline[pop_index_dicc[pop]]
    genotype = genotype_raw.split(':')[0]
    alleles.append(random_geno(genotype,sep))
  #Ignore missing data
  if("." in alleles):
    continue
  #Ignore sites where p3 is not derived and where p1 and p2 have same allele
  #if isAncestral(alleles[2],alleles[3]) or alleles[0] == alleles[1]:
   # continue
  #ABAA:p2 has derived allele
  if (isAncestral(alleles[0],alleles[3])) and (isAncestral(alleles[2],alleles[3])) and alleles[1] != alleles[3]:
    abaa +=1
  #BAAA: p1 has derived allele
  elif alleles[0] != alleles[3] and (isAncestral(alleles[2],alleles[3])):
    baaa +=1
  #Is it ABBA or BABA
  #ABBA: p1 has ancestral allele
  elif(isAncestral(alleles[0],alleles[3])):
    abba += 1
  else(isAncestral(alleles[1],alleles[3])):
    baba += 1
  if(counter%10000==0):
    print("On line {}. ABBA is {}. BABA is {}".format(counter,abba,baba))
file.close()

d_num = (baaa - abaa) + (abba - baba)
d_denom = (baaa + abaa + abba + baba)
#Calculate D
try:
  d = (abba - baba)/(abba + baba)
except ZeroDivisionError:
  d = 'nan'
#Calculate D+
try:
  d_plus = d_num/d_denom
except ZeroDivisionError:
  d_plus = 'nan'

#Things to be outputed
outfile_header="p1\tp2\tp3\tp4\tABBA\tBABA\tABAA\tBAAA\tD\tDPlus\n"
outline = param.p1+"\t"+param.p2+"\t"+param.p3+"\t"+param.p4+"\t"+str(abba) + "\t" + str(baba) + "\t" + str(abaa) + "\t" + str(baaa) + "\t" + str(d) + str(d_plus) + "\n"
#Output results & checking if file already exist
exists = os.path.exists(outfile)
if exists:
  ofile = open(outfile, "a+")
  ofile.write(outline)
  ofile.close()
else:
  fout = open(outfile,"w")
  fout.write(outfile_header)
  fout.write(outline)
  fout.close()


