import sys
import gzip
#when inputing into terminal put python2 p.py vcf.gz gene.vcf.gz chromesome.name start# end#
#input files & outfile
infile= sys.argv[1] #name of vcf
outfile= sys.argv[2] #outfilename
chrom= sys.argv[3] #This input should be the chromosome name
start= sys.argv[4] #This input should be the position at which to start
end= sys.argv[5] #This should be the position at which to end
#opening file
f = gzip.open(infile, 'r')
#opening outfile
outfi = open( outfile, 'w')
#setting a button of sorts to print specfic lines 
alwrite = False
#setting conditions 
startnum=int(start)
endnum=int(end)
chrom_tag=str(chrom)
#Getting header & data
for line in f:
	if line.startswith('##'):
		continue
	if line.startswith('#'):
		outfi.write(line)
		print('Im printing header')
	if chrom_tag in line:
		lii = line.split()
		basenum = int(lii[1])
		if alwrite or basenum >= startnum:
			outfi.write(line)
			alwrite = True
			print('im printing some lines')
		if basenum >= endnum:
			break
#	else:
#		print(line)
#closing outfile
outfi.close()
