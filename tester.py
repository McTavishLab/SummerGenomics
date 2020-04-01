import gzip
import argparse
import math

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--vcf')
    parser.add_argument('--window_size')
    parser.add_argument('--outfile')
    return parser.parse_args()

def main():
    args = parse_args()
    start_pos = 0
    window = int(args.window_size)
    mito_tag = "NC_006853.1"
    f = gzip.open(args.vcf, 'r')
    filename = args.outfile +'_{}.vcf'.format(start_pos)
    ofi = open(filename,'w')
    end_pos= start_pos + window
    line_count = 0
    for line in f:
        if line.startswith("##"):
                continue
        if line.startswith("#CHROM"):
                header = line
                ofi.write(header)
        else:
            if mito_tag in line:
                continue
            if "INDEL" in line:
                continue
            spline = line.split()
            basecall = int(spline[1])
            if start_pos < basecall < end_pos:
                ofi.write(str(line))
                line_count += 1
            elif basecall >= end_pos:
                line_count += 1
                start_pos = math.floor(basecall / window ) * window
                end_pos = start_pos + window
                filename = args.outfile+"_{}.vcf".format(int(start_pos))
                ofi.close()
                ofi = open(filename, 'w')
                ofi.write(header)
                end_pos = start_pos + window
                ofi.write(str(line))
    print("The total number of variant site in the vcf file is "+line_count+".")
    f.close()


if __name__ == '__main__':
    main()
