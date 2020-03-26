import gzip
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--vcf')
    parser.add_argument('--window_size')
    return parser.parse_args()

f = gzip.open(args.vcf, 'r')
 for line in f:
     if line.startswith("##"):
             pass
     if line.startswith("##"):
             header = line
     else:
         vcfrow = line.split('\t')
         if vcfrow[1] - window_size == 0:
             
def main():
    args = parse_args()
