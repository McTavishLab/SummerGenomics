import os

import argparse
parser = argparse.ArgumentParser()                            

parser.add_argument("--map", "-m", type=str, required=True)
parser.add_argument("--input", "-i", type=str, required=True)
parser.add_argument("--output", "-o", type=str, required=True)

args = parser.parse_args()

assert(os.path.exists(args.input))
assert(os.path.exists(args.map))

info = {}

mappings = open(args.map)
header = mappings.readline().strip().split(',')
assert header == ["filename","idnum","individualID","pop"], header


for lin in mappings:
    lii = lin.strip().split(',')
    if len(lii)==4:
        info[lii[0]]={"ind_name":lii[2], 'pop':lii[3]}


fi= open(args.output,'w')
fi.write('filename, ind_name, pop\n')
for samp in open(args.input):
    samp=samp.strip()
    assert(samp in info), samp
    fi.write("{},{},{}\n".format(samp, info[samp]['ind_name'],info[samp]['pop']))


fi.close()