import random
import math

start_pos = 0
window_size = 100


#look at lines in the vcf

#infile = "fake.vcf"
#postions = random.sample(range(1000), 70)

random.seed(3)
inputvcf = random.sample(range(1000),50)

inputvcf.append(100)
inputvcf.append(300)
inputvcf.sort()


print(inputvcf)


file_name = "output_{}.vcf".format(start_pos)
ofi = open(file_name, 'w')
end_pos = start_pos + window_size


for basecall in inputvcf:
#    pos = basecall.split()[1]
    pos = basecall
    if start_pos < pos < end_pos:
#        print("{} is less than {} is less than {}, so it is getting written to {}".format(start_pos, pos, end_pos, file_name))
        ofi.write(str(basecall)+"\n")
    elif pos >= end_pos:
        start_pos = math.floor(pos / window_size) * window_size
        print("{} is geater than {}".format(pos, end_pos))
        end_pos = start_pos + window_size
        file_name = "output_{}.vcf".format(start_pos)
        print("starting a new file named {}, for bases {} to {}".format(file_name, start_pos, end_pos))
        ofi = open(file_name, 'w')
        end_pos = start_pos + window_size
        ofi.write(str(basecall)+"\n")




   