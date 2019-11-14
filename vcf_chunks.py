import sys
import gzip
#when inputing into terminal put python2 p.py vcf.gz gene.vcf.gz chromesome.name start# end#
#input files & outfile
infile= sys.argv[1]#name of vcf
outfile= sys.argv[2]#outfilename
look= sys.argv[3] #This input should be the chromosome name
start= sys.argv[4] #This input should be the position at which to start
end= sys.argv[5]#This should be the position at which to end
#opening file
f = gzip.open(infile, 'r')
#opening outfile
outfi = open(outfile, 'w')
#idk what it actually does pls explain
alwrite = False
#reading file
fr = f.readlines()
#Getting header & data
for line in fr:
	if line.startswith('##'):
		continue
	if line.startswith('#'):
		outfi.write(line)
	if look in line:
		if alwrite or start in line:
			outfi.write(line)
			alwrite = True
		if end in line:
			break
#closing outfile
outfi.close()
