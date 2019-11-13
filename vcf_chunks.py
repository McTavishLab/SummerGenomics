import sys
import gzip 

#input files & outputfile
infile= sys.argv[1]
outfile= sys.argv[2]
look= sys.argv[3]
#opening file 
f = gzip.open(infile, 'r')

#Getting header 
for line in f:
	if line.startswith('#'):
		header = line 
	if look in line:
		store = line 
			 
#opening and writing outfile
outfi = open(outfile, 'w')
outfi.write(header)
outfi.write(store)
outfi.close()