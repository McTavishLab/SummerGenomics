# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 14:46:29 2019

@author: jvela
"""
import sys
inFile = sys.argv[1]

dna =""

with open(inFile) as f:
    firstline = f.readline()
    for line in f:
        dna += line.strip()


length = len(dna)
a_count = dna.count('A')
t_count = dna.count('T')
g_count = dna.count('G')
c_count = dna.count('C')

clist = [] 
dna_count = [a_count, t_count, g_count, c_count]
for count in dna_count:
    percent = float((count )/ float(length)) * 100
    clist.append(str(round(percent, 2)))

print "The header line is %s" % (firstline)
print "The total number of bases in the chromosome is %s" % (length)
print "The percent of A is %s, T is %s, G is %s, and C is %s!" % (clist[0], clist[1], clist[2], clist[3])

